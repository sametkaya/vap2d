# Retraining the Deep Learning Model on a Custom Dataset

VAP2D ships with a pre-trained Faster R-CNN model (ResNet-50 + FPN) optimized for
**cerebral** vessel images. If your data come from a substantially different
modality (e.g. retinal fundus photographs, tumor micro-vasculature, micro-CT),
you can retrain the detector with the standard [Detectron2](https://github.com/facebookresearch/detectron2)
pipeline and plug the new weights back into VAP2D.

## How VAP2D loads the model

At inference time (`DeepLearning/DeepLearningObjectDetection.py`) VAP2D reads, relative to the repository root:

- **Config:** `detectron2/model/faster_rcnn_R_50_FPN_1x.yaml`
- **Weights:** `DeepLearning/Train/model_final.pth`
- **Classes:** 2 categories, labelled `"T"` (tip / endpoint) and `"B"` (branch point)
- **Dataset name (metadata):** `my_coco_dataset`

So the goal of retraining is to produce a new `model_final.pth` and place it at
`DeepLearning/Train/model_final.pth`. Keep the two-class T/B convention so the
rest of VAP2D works unchanged.

## Workflow overview

1. **Prepare images.** If they are not already binary single-pixel-wide
   skeletons, run them through the VAP2D pre-processing pipeline
   (Denoise → Segment → Skeletonize) so the inputs match what the detector
   expects.
2. **Generate annotations (COCO format).** Two options:
   - **Automatic:** use the built-in TIP (Hit-or-Miss) detector to produce
     branch-point and endpoint boxes (5x5 px), then export to COCO JSON.
   - **Manual:** label with [labelme](https://github.com/wkentaro/labelme) or
     [CVAT](https://github.com/opencv/cvat) and export to COCO.
   Use category id/name **`B`** for branch points and **`T`** for tips.
3. **Split** into `train/` and `test/`, each with its own `annotations.json`.
4. **Register** the datasets with Detectron2.
5. **Configure and train**, starting from the bundled hyperparameters.
6. **Export** the weights to `DeepLearning/Train/model_final.pth`.

## Expected dataset layout

```
my_dataset/
├── train/
│   ├── images/                 # binary skeleton images
│   └── annotations.json        # COCO annotations (categories: T, B)
└── test/
    ├── images/
    └── annotations.json
```

## Step 4 — Register the datasets

```python
from detectron2.data.datasets import register_coco_instances

register_coco_instances(
    "my_coco_dataset_train", {},
    "my_dataset/train/annotations.json", "my_dataset/train/images",
)
register_coco_instances(
    "my_coco_dataset_test", {},
    "my_dataset/test/annotations.json", "my_dataset/test/images",
)
```

## Step 5 — Reference training configuration

These are the optimized hyperparameters used for the bundled cerebral-vessel
model and are a sensible starting point. Tune them for your data and hardware.

```python
import os
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer

cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml")
)
cfg.DATASETS.TRAIN = ("my_coco_dataset_train",)
cfg.DATASETS.TEST = ("my_coco_dataset_test",)
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml"
)

# --- Optimized hyperparameters (same as the bundled model) ---
cfg.SOLVER.BASE_LR = 0.01          # base learning rate
cfg.SOLVER.MAX_ITER = 10000        # maximum iterations
cfg.SOLVER.IMS_PER_BATCH = 128     # lower this if you run out of GPU memory

cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2          # T (tip), B (branch)
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
# Small 5x5 boxes -> keep many proposals, as the inference code does:
cfg.MODEL.RPN.PRE_NMS_TOPK_TRAIN = 15000
cfg.MODEL.RPN.POST_NMS_TOPK_TRAIN = 15000

# cfg.MODEL.DEVICE = "cpu"   # uncomment if you have no CUDA GPU

cfg.OUTPUT_DIR = "./output_retrained"
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()
# weights are written to ./output_retrained/model_final.pth
```

## Step 6 — Install the new model into VAP2D

```bash
cp ./output_retrained/model_final.pth DeepLearning/Train/model_final.pth
```

Then select the **Deep Learning** method in the application (or pass
`--method dl` to `batch_analyze.py`). The hybrid TIP-based center localization is
applied automatically on top of the DL detections, so a retrained model benefits
from the same sub-pixel localization as the bundled one.

## Tips

- If detection quality is poor, first verify the skeletons are genuinely
  single-pixel-wide and gap-free — most failures originate in pre-processing.
- For small datasets, reduce `MAX_ITER` and watch the validation AP to avoid
  overfitting.
- Lower `IMS_PER_BATCH` (e.g. 16 or 32) on memory-constrained GPUs.
