# Retraining the Deep Learning Model on a Custom Dataset

VAP2D ships with a pre-trained Faster R-CNN model (ResNet-50 + FPN) optimized for
**cerebral** vessel images. If your data come from a substantially different
modality (e.g. retinal fundus photographs, tumor micro-vasculature, micro-CT),
you can retrain the detector with the standard [Detectron2](https://github.com/facebookresearch/detectron2)
pipeline and plug the new weights back into VAP2D.

> The Python snippets below are **reference templates**. Adapt the import paths and
> directory names to match your local checkout. The Detectron2 configuration is the
> stable part; the VAP2D-specific glue (loading the resulting `.pth`) is described in
> the last step.

## Overview of the workflow

1. **Prepare images.** Collect the target images. If they are not already binary
   single-pixel-wide skeletons, run them through the same VAP2D pre-processing
   pipeline (Denoise → Segment → Skeletonize) so the inputs match what the
   detector expects.

2. **Generate annotations (COCO format).** You have two options:
   - **Automatic:** use the built-in TIP (Hit-or-Miss) detector to produce
     branch-point and endpoint boxes (`5x5` pixels), then export them to a COCO
     JSON file. This is the fastest way to bootstrap a labelled set on clean
     binary skeletons.
   - **Manual:** label branch points and endpoints with a tool such as
     [labelme](https://github.com/wkentaro/labelme) or
     [CVAT](https://github.com/opencv/cvat) and export to COCO format.

3. **Split the data** into `train/` and `test/` sets, each with its own
   `annotations.json` (COCO).

4. **Register the datasets** with Detectron2.

5. **Configure and train** a Faster R-CNN model, starting from the hyperparameters
   that worked well for the bundled model.

6. **Export and install** the trained weights into VAP2D.

## Expected dataset layout

```
my_dataset/
├── train/
│   ├── images/                 # binary skeleton images
│   └── annotations.json        # COCO annotations for the train split
└── test/
    ├── images/
    └── annotations.json
```

The COCO file must contain two categories, e.g. `branch_point` and `end_point`,
with `5x5` pixel bounding boxes centered on each detected point.

## Step 4 — Register the datasets

```python
from detectron2.data.datasets import register_coco_instances

register_coco_instances(
    "vap2d_train", {},
    "my_dataset/train/annotations.json",
    "my_dataset/train/images",
)
register_coco_instances(
    "vap2d_test", {},
    "my_dataset/test/annotations.json",
    "my_dataset/test/images",
)
```

## Step 5 — Reference training configuration

These values are the optimized hyperparameters used for the bundled cerebral-vessel
model and are a sensible starting point. Tune `BASE_LR`, `MAX_ITER` and the batch
size for your own data and hardware.

```python
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer
import os

cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
)
cfg.DATASETS.TRAIN = ("vap2d_train",)
cfg.DATASETS.TEST = ("vap2d_test",)
cfg.DATALOADER.NUM_WORKERS = 2

# Start from COCO-pretrained weights
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
)

# --- Optimized hyperparameters (same as the bundled model) ---
cfg.SOLVER.BASE_LR = 0.01          # base learning rate
cfg.SOLVER.MAX_ITER = 10000        # maximum iterations
cfg.SOLVER.IMS_PER_BATCH = 128     # batch size per image (lower this if you run out of memory)

cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2   # branch_point, end_point
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128

# Use CPU if no CUDA GPU is available
# cfg.MODEL.DEVICE = "cpu"

cfg.OUTPUT_DIR = "./output_retrained"
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()
```

After training, the weights are written to
`./output_retrained/model_final.pth`.

## Step 6 — Install the new model into VAP2D

Copy the trained checkpoint into the VAP2D model directory and select the
**Deep Learning** method in the application. VAP2D will then use your retrained
model for branch-point and endpoint detection.

```bash
cp ./output_retrained/model_final.pth <VAP2D_MODEL_DIRECTORY>/
```

> Replace `<VAP2D_MODEL_DIRECTORY>` with the directory from which VAP2D loads its
> model weights in your installation. The hybrid post-processing (TIP-based center
> localization) is applied automatically on top of the DL detections, so retrained
> models benefit from the same sub-pixel localization as the bundled model.

## Tips

- If detection quality is poor, first check that your skeletons are genuinely
  single-pixel-wide and free of large gaps — most failures come from the
  pre-processing stage, not the detector.
- For small datasets, reduce `MAX_ITER` and watch the validation AP to avoid
  overfitting.
- Lower `IMS_PER_BATCH` (e.g. to 16 or 32) if you hit GPU out-of-memory errors.
