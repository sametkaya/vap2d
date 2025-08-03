from collections import deque

import numpy as np
import cv2
from GraphicItems.VAP_Point import VAP_Point, VAP_Point_Type
from GraphicItems.VAP_Vein import VAP_Vein
from System import FilterKernels
from detectron2.config import get_cfg
#from detectron2 import DefaultPredictor
from detectron2.data import MetadataCatalog
from pathlib import Path

from detectron2.engine import DefaultPredictor


def predict_objects_from_image(image_skel_uint8):
    """
    Predicts objects in the given preprocessed image and returns the bounding box coordinates.

    :param image_skel_uint8: Preprocessed image (binary skeletonized image).
    :return: List of bounding boxes in [x_min, y_min, x_max, y_max] format.
    """
    pad_width = 2
    image_skel_padded = np.pad(image_skel_uint8, pad_width=pad_width, mode='constant', constant_values=0)
    # Convert grayscale to 3-channel image if necessary
    if len(image_skel_padded.shape) == 2:
        image_skel_padded = cv2.cvtColor(image_skel_padded, cv2.COLOR_GRAY2BGR)

    image_skel_padded = image_skel_padded.astype(np.uint8)
    assert image_skel_padded.shape[2] == 3, "Image should have 3 channels (BGR format)."
    assert image_skel_padded.dtype == np.uint8, "Image dtype should be np.uint8."

    # Initialize configuration
    home = Path.cwd()
    model_path = home / "detectron2" / "model" / "faster_rcnn_R_50_FPN_1x.yaml"
    cfg = get_cfg()
    cfg.merge_from_file(str(model_path))
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.TEST.DETECTIONS_PER_IMAGE = 10000
    cfg.MODEL.RPN.POST_NMS_TOPK_TEST = 15000
    cfg.MODEL.RPN.PRE_NMS_TOPK_TEST = 15000
    cfg.MODEL.RPN.POST_NMS_TOPK_TRAIN = 15000
    cfg.MODEL.RPN.PRE_NMS_TOPK_TRAIN = 15000
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.7
    model_weights= str(home / "DeepLearning" / "Train" / "model_final.pth")
    cfg.MODEL.WEIGHTS = model_weights
    # Get class labels from metadata
    metadata = MetadataCatalog.get("my_coco_dataset")  # Ensure dataset is registered
    class_labels = metadata.thing_classes if hasattr(metadata, "thing_classes") else ["T", "B"]
    # Initialize the predictor
    predictor = DefaultPredictor(cfg)
    # Convert to float32 for processing
    image_skel_float32 = image_skel_padded.astype(np.float32)
    # Run prediction
    outputs = predictor(image_skel_float32)

    # Extract bounding boxes and class labels
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Bounding box coordinates: [x_min, y_min, x_max, y_max]
    class_indices = instances.pred_classes.numpy()  # Predicted class indices

    # Format output as [(x_min, y_min, x_max, y_max, class_label), ...]
    objects = [
        (int(np.floor(x_min))-pad_width, int(np.floor(y_min))-pad_width, int(np.ceil(x_max))-pad_width, int(np.ceil(y_max))-pad_width, class_labels[class_idx])
        for (x_min, y_min, x_max, y_max), class_idx in zip(boxes, class_indices)
    ]

    return objects


def Analayze(image_skel_uint8, refined_results):
    """
    :param image_skel_uint8: Skeletonized binary image.
    :param refined_results: List of refined bounding boxes [(x_min, y_min, x_max, y_max, class_label), ...]
    :return: Tuple of lists (vap_branch_list, vap_tip_list)
    """

    # Ensure input image is binary (0 or 255)
    image_skel_uint8 = (image_skel_uint8 > 0).astype(np.uint8) * 255


    branch_points_kernels = FilterKernels.BranchPointKernels()

    tip_points_kernels = FilterKernels.TipPointKernels()

    # Pad the skeleton image to prevent border issues
    image_skel_padded = np.pad(image_skel_uint8, pad_width=1, mode='constant', constant_values=0)
    image_points_padded = (image_skel_padded > 0).astype(np.uint8)
    vap_branch_list = []
    vap_tip_list = []
    points=[]

    # Process each detected object in `refined_results`
    for (x_min, y_min, x_max, y_max, class_label) in refined_results:
        # Extract local search region
        bbox_region = image_skel_padded[y_min:y_max, x_min:x_max]

        if bbox_region.size == 0:
            continue

        if class_label == "B":  # Branch Point Detection in boundbox
            bbox_region = np.pad(bbox_region, pad_width=1, mode='constant', constant_values=0)
            for kernel in branch_points_kernels:
                branch_response = cv2.morphologyEx(bbox_region, cv2.MORPH_HITMISS, kernel)
                # Find contours
                branch_objects, _ = cv2.findContours(branch_response, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(branch_objects) > 0:

                    branch_x, branch_y = branch_objects[0][0][0]  # Extract first contour point
                    refined_x = x_min + branch_x - 2 # because one more path, one pah image path, one bound box path
                    refined_y = y_min + branch_y - 2
                    if image_points_padded[refined_y + 1, refined_x + 1] == 1:
                        vap_branch_list.append(VAP_Point(refined_y, refined_x, VAP_Point_Type.BRANCH))
                        points.append((refined_y+1, refined_x+1))
                        image_points_padded[refined_y+1, refined_x+1] += 2
                    break  # Stop searching after the first match

        elif class_label == "T":  # Tip Point Detection in boundbox
            bbox_region = np.pad(bbox_region, pad_width=1, mode='constant', constant_values=255)
            for kernel in tip_points_kernels:
                tip_response = cv2.morphologyEx(bbox_region,  op=cv2.MORPH_HITMISS, kernel=kernel,borderType=cv2.BORDER_CONSTANT, borderValue=1)
                # Find contours
                tip_objects, _ = cv2.findContours(tip_response, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(tip_objects) > 0:
                    tip_x, tip_y = tip_objects[0][0][0]  # Extract first contour point
                    refined_x = x_min + tip_x-2
                    refined_y = y_min + tip_y-2
                    if image_points_padded[refined_y + 1, refined_x + 1] == 1:
                        vap_tip_list.append(VAP_Point(refined_y, refined_x, VAP_Point_Type.TIP))
                        points.append((refined_y+1, refined_x+1))
                        image_points_padded[refined_y+1, refined_x+1] += 1
                    break  # Stop searching after the first match


    #find vein path
    drawed_skel_img_padded = np.zeros(image_skel_padded.shape[:2], dtype=np.uint16)
    # All 8 directions
    # delta = [(-1, -1), (-1, 0), (-1, 1),
    #         (0, -1), (0, 1),
    #         (1, -1), (1, 0), (1, 1)]

    # vein direction
    delta = [(-1, 0), (0, 1), (0, -1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    vap_vein_list = []
    point_id = 1
    for point in points:
        y, x = point

        if (drawed_skel_img_padded[y][x] == VAP_Point_Type.NONE.value):
            scan_veins_bfs = deque([])
            if (image_points_padded[y][x] == VAP_Point_Type.BRANCH.value):  # if branch point
                vap_branch_point = VAP_Point(y - 1, x - 1, VAP_Point_Type.BRANCH)
                for dy, dx in delta:
                    yy, xx = y + dy, x + dx
                    # If the next position hasn't already been looked at and it's white
                    # sonraki posizyona bakılmamışsa ve işaretlenmemişse
                    if image_points_padded[yy][xx] > 0 and drawed_skel_img_padded[yy][xx] == 0:
                        # vap_vein = VAP_Vein()
                        scan_vein = VAP_Vein(point_id)
                        point_id = point_id + 1
                        vap_point = VAP_Point(yy - 1, xx - 1, image_points_padded[yy][xx])
                        scan_vein.branch_points.append(vap_branch_point)
                        scan_vein.vap_point_list.append(vap_point)
                        drawed_skel_img_padded[yy][xx] = scan_vein.idn
                        scan_veins_bfs.append(scan_vein) # add all points for searching around breach point

            elif (image_points_padded[y][x] == VAP_Point_Type.TIP.value):  # if tip point
                vap_point = VAP_Point(y -1, x-1 , VAP_Point_Type.TIP)
                scan_vein = VAP_Vein(point_id)
                point_id = point_id + 1
                scan_vein.vap_point_list.append(vap_point)
                scan_vein.tip_points.append(vap_point)
                drawed_skel_img_padded[y][x] = VAP_Point_Type.TIP.value
                scan_veins_bfs.append(scan_vein) #tip point only has one neighbor
            else:
                vap_point = VAP_Point(y - 1, x - 1, VAP_Point_Type.PATH)
                # vap_vein = VAP_Vein()
                scan_vein = VAP_Vein(point_id)
                point_id = point_id + 1
                scan_vein.vap_point_list.append(vap_point)
                drawed_skel_img_padded[y][x] = scan_vein.idn
                scan_veins_bfs.append(scan_vein)

            while len(scan_veins_bfs) > 0:
                scan_vein = scan_veins_bfs.popleft()
                vap_point = scan_vein.vap_point_list[0]
                padded_point = VAP_Point(vap_point.y + 1, vap_point.x + 1, vap_point.vp_type)
                vap_point_bfs = deque([padded_point])
                while len(vap_point_bfs) > 0:

                    p = vap_point_bfs.popleft()

                    for dy, dx in delta:  # directions
                        yy, xx = p.y + dy, p.x + dx



                        if (image_points_padded[yy][xx] > 0 and drawed_skel_img_padded[yy][xx] == 0):

                            if (image_points_padded[yy][xx] == VAP_Point_Type.PATH.value):

                                is_end=False
                                # tespit edilmemiş dallanma ve uç noktaları bulmak için
                                # region = image_points_padded[yy - 1:yy + 2, xx - 1:xx + 2]
                                # padded_region = np.zeros((3, 3), dtype=np.uint8)
                                # padded_region[:region.shape[0], :region.shape[1]] = region
                                # is_end=False
                                # for kernel in branch_points_kernels:
                                #     hit_or_miss = cv2.morphologyEx(padded_region, cv2.MORPH_HITMISS, kernel)
                                #     if hit_or_miss[1, 1] == 1:
                                #         vap_point = VAP_Point(yy - 1, xx - 1, VAP_Point_Type.BRANCH)
                                #         if (vap_point in scan_vein.branch_points):
                                #             continue
                                #         drawed_skel_img_padded[yy][xx] = VAP_Point_Type.BRANCH.value
                                #         scan_vein.branch_points.append(vap_point)
                                #         scan_vein.vap_point_list.append(vap_point)
                                #         is_end=True
                                #         break
                                #
                                # for kernel in tip_points_kernels:
                                #     hit_or_miss = cv2.morphologyEx(padded_region, cv2.MORPH_HITMISS, kernel)
                                #     if hit_or_miss[1, 1] == 1:
                                #
                                #         vap_point = VAP_Point(yy - 1, xx - 1, VAP_Point_Type.TIP)
                                #         if (vap_point in scan_vein.tip_points):
                                #             continue
                                #         drawed_skel_img_padded[yy][xx] = VAP_Point_Type.TIP.value
                                #         scan_vein.tip_points.append(vap_point)
                                #         scan_vein.vap_point_list.append(vap_point)
                                #         is_end = True
                                #         break

                                # son
                                if not is_end:
                                    drawed_skel_img_padded[yy][xx] = scan_vein.idn
                                    vap_point = VAP_Point(yy - 1, xx - 1, VAP_Point_Type.PATH)

                                    scan_vein.vap_point_list.append(vap_point)
                                    next_vap_point = VAP_Point(yy, xx, VAP_Point_Type(image_points_padded[yy][xx]))
                                    vap_point_bfs.append(next_vap_point)
                                break
                            elif (image_points_padded[yy][xx] == VAP_Point_Type.TIP.value):
                                drawed_skel_img_padded[yy][xx] = VAP_Point_Type.TIP.value
                                vap_point = VAP_Point(yy - 1, xx - 1, VAP_Point_Type.TIP)
                                if (vap_point in scan_vein.tip_points):
                                    continue
                                scan_vein.tip_points.append(vap_point)
                                scan_vein.vap_point_list.append(vap_point)
                                break
                            elif (image_points_padded[yy][xx] == VAP_Point_Type.BRANCH.value):

                                vap_point = VAP_Point(yy - 1, xx - 1, VAP_Point_Type.BRANCH)
                                if (vap_point in scan_vein.branch_points and len(scan_vein.vap_point_list) < 2):
                                    continue
                                scan_vein.branch_points.append(vap_point)
                                scan_vein.vap_point_list.append(vap_point)
                                break
                scan_vein.Build_Up()
                if (len(scan_vein.vap_point_list) > 1) or (len(scan_vein.branch_points) > 1):
                    scan_vein.idn = len(vap_vein_list) + 1
                    vap_vein_list.append(scan_vein)

    return vap_vein_list, vap_branch_list, vap_tip_list








