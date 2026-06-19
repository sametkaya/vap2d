"""
batch_analyze.py -- Headless batch analysis for VAP2D.

Runs the same analysis pipeline as the GUI over every image in a folder and
writes one CSV + PDF report per image, WITHOUT opening the graphical interface.
It calls VAP2D's real functions directly:

    System.ImageProcessing.GetImageFormats / DenoiseImage / Segment /
        RemoveSmallObject / Skeletonize / GetVascularAreaFractionValues / Analyze
    System.ImageOperation.ImageOperation.SaveCsv / SaveAsPdf

Place this file in the repository ROOT (next to main.py) and run it from there:

    # Already-binary skeleton images (e.g. the bundled sample data), TIP method:
    python batch_analyze.py --input Sample_Data/HFHS13 --output batch_reports --binary

    # Raw grayscale images that still need pre-processing:
    python batch_analyze.py --input my_raw_images --output batch_reports

    # Use the deep-learning detector instead of TIP (needs the trained model,
    # see docs/RETRAINING.md):
    python batch_analyze.py --input Sample_Data/HFHS13 --output batch_reports --binary --method dl
"""
import os
import sys
import glob
import argparse
from types import SimpleNamespace

# Make the project packages importable when run from the repository root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from System import ImageProcessing
from System.ImageOperation import ImageOperation


def analyze_one(image_path, output_dir, method="tip", already_binary=True):
    """Analyse a single image and write its CSV + PDF report. Returns the paths."""
    name = os.path.basename(image_path)

    # 1) Load. GetImageFormats returns (raw BGR, grayscale uint8).
    #    In the GUI, vap_image.image_byte8 == the grayscale image.
    image_raw, image_gray = ImageProcessing.GetImageFormats(image_path)
    image_byte8 = image_gray

    # 2) Pre-processing. Skip entirely for inputs that are already binary
    #    skeletons; otherwise run the same chain the GUI buttons run.
    if not already_binary:
        image_byte8 = ImageProcessing.DenoiseImage(image_byte8)
        image_byte8 = image_byte8.reshape(image_byte8.shape[0], image_byte8.shape[1])
        image_byte8 = ImageProcessing.Segment(image_byte8)
        image_byte8 = ImageProcessing.RemoveSmallObject(image_byte8)
        image_byte8 = ImageProcessing.Skeletonize(image_byte8)

    # 3) Vascular area fraction (deterministic; computed for both methods here).
    vaf, white_px, black_px = ImageProcessing.GetVascularAreaFractionValues(image_byte8)

    # 4) Detection + vascular-graph construction.
    if method == "dl":
        # DL path: needs DeepLearning/Train/model_final.pth and the registered
        # dataset. Imported lazily so the TIP path has no detectron2 dependency.
        from DeepLearning import DeepLearningObjectDetection as DL
        predicted = DL.predict_objects_from_image(image_byte8)
        vap_veins, branch_points, tip_points = DL.Analayze(image_byte8, predicted)
    else:  # "tip"
        vap_veins, branch_points, tip_points = ImageProcessing.Analyze(image_byte8)

    # 5) Aggregate metrics. In the GUI these are accumulated by the graphics
    #    scene (VAP_Image.AddVein); headless, we compute them directly. Each
    #    VAP_Vein already has .length set by Analyze() -> Build_Up().
    total_len = sum(v.length for v in vap_veins)
    avg_len = (total_len / len(vap_veins)) if vap_veins else 0

    # 6) Build a lightweight stand-in exposing exactly the attributes that
    #    SaveCsv / SaveAsPdf read from a VAP_Image. This is the whole trick:
    #    the reporting code never needs the GUI, only these fields.
    vap_image = SimpleNamespace(
        image_raw_name=name,
        vascularAreaFraction=vaf,
        whitePixelCount=white_px,
        blackPixelCount=black_px,
        branchPoints=branch_points,
        tipPoints=tip_points,
        vap_veins=vap_veins,
        total_vein_length=total_len,
        average_vein_length=avg_len,
    )

    # 7) Same information set the GUI 'Report' button enables.
    information_dict = {
        "vaf(%)": True, "id": True,
        "branch points count": True, "tip point count": True,
        "vein count": True, "total vein length": True,
        "average vein length": True,
        "p1.x, p1.y": True, "p2.x, p2.y": True, "length": True,
        "p1_type": True, "p2_type": True,
    }

    report_name = f"{method}_{os.path.splitext(name)[0]}"
    # Call SaveCsv/SaveAsPdf directly with an explicit folder. (SaveInfos is the
    # GUI entry point and would pop a folder-picker dialog -- we bypass it.)
    csv_path = ImageOperation.SaveCsv(vap_image, output_dir, report_name, information_dict)
    pdf_path = ImageOperation.SaveAsPdf(vap_image, output_dir, report_name, information_dict)
    return csv_path, pdf_path


def main():
    parser = argparse.ArgumentParser(
        description="Batch VAP2D analysis (headless, no GUI)."
    )
    parser.add_argument("--input", required=True, help="folder containing input images")
    parser.add_argument("--output", default="batch_reports", help="folder for the reports")
    parser.add_argument("--method", choices=["tip", "dl"], default="tip",
                        help="detection method: tip (default) or dl")
    parser.add_argument("--binary", action="store_true",
                        help="inputs are already binary skeletons (skip pre-processing)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    patterns = ("*.tif", "*.tiff", "*.png", "*.bmp", "*.jpg", "*.jpeg")
    paths = sorted(p for pat in patterns
                   for p in glob.glob(os.path.join(args.input, pat)))

    if not paths:
        print(f"No images found in '{args.input}'.")
        return

    print(f"Found {len(paths)} image(s). Method={args.method}. "
          f"Writing reports to '{args.output}/'.")
    ok = 0
    for path in paths:
        try:
            csv_path, _ = analyze_one(
                path, args.output, method=args.method, already_binary=args.binary
            )
            ok += 1
            print(f"  OK   {os.path.basename(path)} -> {os.path.basename(csv_path)}")
        except Exception as e:
            print(f"  FAIL {os.path.basename(path)}: {e}")
    print(f"Done. {ok}/{len(paths)} succeeded.")


if __name__ == "__main__":
    main()
