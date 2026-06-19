# Batch / Scripted Processing

VAP2D is primarily a GUI application, but its analysis logic lives in the
`System/` layer and is **decoupled from the interface**. This means the
pre-processing, detection, graph-construction and export routines can be called
directly from a Python script — useful for processing a whole folder of images
without manual interaction, or for embedding VAP2D as a quantification step in a
larger pipeline.

> ⚠️ **This is an illustrative template.** The exact class and method names below
> should be matched to the functions in your `System/` modules (e.g.
> `System/ImageOperation.py`). Use it as a starting skeleton and wire in the real
> calls from your codebase. There is no separate command-line interface in the
> current release; this script *is* the recommended way to run VAP2D headlessly.

## Example: process every image in a directory

```python
"""
Batch-process a folder of vessel images with VAP2D and write one
CSV/PDF report per image. Adapt the imports and calls to your System/ API.
"""
import os
import glob

# --- Import the VAP2D analysis layer (adapt paths to your project) ---
# from System.ImageOperation import ImageOperation
# from System.VapImage import VapImage          # object that holds image + results

INPUT_DIR  = "Sample_Data/HFHS13"   # folder of input images
OUTPUT_DIR = "batch_reports"        # where reports are written
METHOD     = "tip"                  # "tip" (traditional) or "dl" (deep learning)

os.makedirs(OUTPUT_DIR, exist_ok=True)

image_paths = sorted(
    glob.glob(os.path.join(INPUT_DIR, "*.tif"))
    + glob.glob(os.path.join(INPUT_DIR, "*.png"))
)

for path in image_paths:
    name = os.path.splitext(os.path.basename(path))[0]
    print(f"Processing {name} ...")

    # 1) Load the image into a VAP image object
    #    vap_image = VapImage(path)

    # 2) Optional pre-processing (skip if the input is already a binary skeleton)
    #    vap_image.denoise()
    #    vap_image.segment()
    #    vap_image.skeletonize()

    # 3) Detect branch points and endpoints with the chosen method
    #    vap_image.detect(method=METHOD)

    # 4) Build the vascular graph and compute metrics (paths, lengths, density)
    #    vap_image.analyse()

    # 5) Export the per-image report (CSV + PDF)
    #    information_dict = { ... }   # same fields the GUI 'Report' button sets
    #    ImageOperation.SaveInfos(vap_image, information_dict, report_type=METHOD)

    # (Move/rename the produced report into OUTPUT_DIR as needed.)

print("Done.")
```

## Aggregating results across a cohort

Because each run writes a flat CSV, results for an entire dataset can be combined
for statistical analysis:

```python
import glob
import pandas as pd

frames = []
for csv_path in glob.glob("batch_reports/*.csv"):
    df = pd.read_csv(csv_path)
    df["source_image"] = csv_path
    frames.append(df)

cohort = pd.concat(frames, ignore_index=True)
cohort.to_csv("cohort_summary.csv", index=False)
print(cohort.describe())
```

## Pipeline integration

Because the analysis layer operates on standard skeletonized inputs, VAP2D can be
dropped in as a **quantification back-end** after an upstream segmentation tool
(e.g. Fiji/ImageJ, napari, or a custom U-Net): export binary skeletons from the
upstream tool, point the batch script at that folder, and collect the aggregated
metrics for downstream analysis.

## Roadmap

A thin command-line entry point and an optional lightweight REST endpoint are
planned, building on the same `System/` routines used above. Contributions toward
these are welcome — see [`SUPPORT.md`](../../../../Downloads/vap2d_repo_support_files/SUPPORT.md).
