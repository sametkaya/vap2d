# Batch / Scripted Processing

VAP2D is primarily a GUI application, but its analysis logic lives in the
`System/` layer and is **fully decoupled from the interface**. The
pre-processing, detection, vascular-graph construction and CSV/PDF export
routines can be imported and called directly from a Python script — useful for
processing a whole folder of images without manual interaction, or for embedding
VAP2D as a quantification step in a larger pipeline.

The repository includes a ready-to-run script, **`batch_analyze.py`** (in the
repository root). It uses the same functions the GUI uses:

| Stage | GUI action | Function called |
| --- | --- | --- |
| Load image | *Load Image* | `System.ImageProcessing.GetImageFormats` |
| Denoise | *Denoise* | `System.ImageProcessing.DenoiseImage` |
| Segment | *Segment* | `System.ImageProcessing.Segment` + `RemoveSmallObject` |
| Skeletonize | *Skeletonize* | `System.ImageProcessing.Skeletonize` |
| Detect (TIP) | *Analyse* (Img Processing) | `System.ImageProcessing.Analyze` |
| Detect (DL) | *Analyse* (Deep Learning) | `DeepLearning.DeepLearningObjectDetection.predict_objects_from_image` + `Analayze` |
| Report | *Report* | `System.ImageOperation.ImageOperation.SaveCsv` / `SaveAsPdf` |

## Usage

Run from the repository root (next to `main.py`):

```bash
# Already-binary skeleton images (e.g. the bundled sample data), TIP method:
python batch_analyze.py --input Sample_Data/HFHS13 --output batch_reports --binary

# Raw grayscale images that still need pre-processing:
python batch_analyze.py --input my_raw_images --output batch_reports

# Deep-learning detector instead of TIP (needs the trained model, see RETRAINING.md):
python batch_analyze.py --input Sample_Data/HFHS13 --output batch_reports --binary --method dl
```

Each input image produces `tip_<name>.csv` / `tip_<name>.pdf` (or `dl_<name>.*`)
in the output folder — the same reports the GUI's *Report* button generates.

## How it works (the key idea)

The only GUI-specific object in the analysis flow is `VAP_Image`, which the
graphics scene fills in. The reporting code (`SaveCsv` / `SaveAsPdf`) does **not**
need the GUI — it only reads a handful of plain attributes from that object:
`image_raw_name`, `vascularAreaFraction`, `branchPoints`, `tipPoints`,
`vap_veins`, `total_vein_length`, and `average_vein_length`.

So the script simply (1) calls the `ImageProcessing` functions to get the veins,
branch points and tip points, (2) computes the aggregate lengths, and (3) packs
those values into a lightweight `SimpleNamespace` stand-in that is handed to
`SaveCsv` / `SaveAsPdf`. No `QApplication` and no windows are required.

```python
import os, glob
from types import SimpleNamespace
from System import ImageProcessing
from System.ImageOperation import ImageOperation

def analyze_one(image_path, output_dir, already_binary=True):
    name = os.path.basename(image_path)

    # 1) load -> grayscale (== image_byte8 in the GUI)
    _, image_gray = ImageProcessing.GetImageFormats(image_path)
    image_byte8 = image_gray

    # 2) pre-process only if needed
    if not already_binary:
        image_byte8 = ImageProcessing.DenoiseImage(image_byte8)
        image_byte8 = image_byte8.reshape(image_byte8.shape[0], image_byte8.shape[1])
        image_byte8 = ImageProcessing.Segment(image_byte8)
        image_byte8 = ImageProcessing.RemoveSmallObject(image_byte8)
        image_byte8 = ImageProcessing.Skeletonize(image_byte8)

    # 3) metrics + detection
    vaf, white_px, black_px = ImageProcessing.GetVascularAreaFractionValues(image_byte8)
    vap_veins, branch_points, tip_points = ImageProcessing.Analyze(image_byte8)

    total_len = sum(v.length for v in vap_veins)
    avg_len = total_len / len(vap_veins) if vap_veins else 0

    # 4) stand-in for VAP_Image -- only the fields the report writers read
    vap_image = SimpleNamespace(
        image_raw_name=name, vascularAreaFraction=vaf,
        whitePixelCount=white_px, blackPixelCount=black_px,
        branchPoints=branch_points, tipPoints=tip_points,
        vap_veins=vap_veins, total_vein_length=total_len,
        average_vein_length=avg_len,
    )

    info = {"vaf(%)": True, "id": True, "branch points count": True,
            "tip point count": True, "vein count": True,
            "total vein length": True, "average vein length": True,
            "p1.x, p1.y": True, "p2.x, p2.y": True, "length": True,
            "p1_type": True, "p2_type": True}

    report_name = f"tip_{os.path.splitext(name)[0]}"
    ImageOperation.SaveCsv(vap_image, output_dir, report_name, info)
    ImageOperation.SaveAsPdf(vap_image, output_dir, report_name, info)
```

> Tip: test on a single image first. If detection looks wrong, check that the
> input is a genuine single-pixel-wide binary skeleton — most issues come from
> the pre-processing stage, not the detector.

## Aggregating results across a cohort

Because each run writes a flat CSV, results for an entire dataset can be combined:

```python
import glob
import pandas as pd

frames = []
for csv_path in glob.glob("batch_reports/tip_*.csv"):
    df = pd.read_csv(csv_path, nrows=1)   # first row = per-image summary
    df["source_image"] = csv_path
    frames.append(df)

cohort = pd.concat(frames, ignore_index=True)
cohort.to_csv("cohort_summary.csv", index=False)
print(cohort.describe())
```

## Pipeline integration

Because the analysis layer operates on standard skeletonized inputs, VAP2D can be
dropped in as a **quantification back-end** after an upstream segmentation tool
(Fiji/ImageJ, napari, or a custom U-Net): export binary skeletons from the
upstream tool, point `batch_analyze.py` at that folder with `--binary`, and
collect the aggregated metrics for downstream analysis.

## Roadmap

A thin command-line entry point (this script) is provided; an optional
lightweight REST endpoint building on the same `System/` routines is a planned
extension. Contributions are welcome — see [`SUPPORT.md`](../SUPPORT.md).
