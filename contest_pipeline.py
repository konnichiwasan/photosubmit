#!/usr/bin/env python3
"""
contest_pipeline.py — Photo Contest Submission Pipeline
========================================================
Scans a folder of photos, excludes images containing faces,
applies enhancement (strong or light), strips GPS metadata,
and writes ready-to-submit exports.

Usage
-----
    # Strong enhancement (punchy contrast/colour for nature/landscape contests)
    python3 contest_pipeline.py --enhance strong

    # Light enhancement (subtle; for contests requiring minimal processing)
    python3 contest_pipeline.py --enhance light --out submission_ready_light

Requirements
------------
    pip install opencv-python-headless pillow piexif

Configuration
-------------
Edit the constants below to match your setup.
"""

import argparse
import sys
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

# Folder containing your source photos
PHOTOS_DIR = Path(__file__).parent / "photos"

# Default output folder (created if it doesn't exist)
DEFAULT_OUT = Path(__file__).parent / "submission_ready"

# Image extensions to process
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# Face detection confidence threshold (0–1). Higher = stricter exclusion.
# Set to None to disable face detection entirely.
FACE_THRESHOLD = 0.5

# Enhancement presets
PRESETS = {
    "strong": {
        "contrast":   1.30,
        "color":      1.25,
        "sharpness":  1.50,
        "brightness": 1.05,
    },
    "light": {
        "contrast":   1.10,
        "color":      1.08,
        "sharpness":  1.20,
        "brightness": 1.00,
    },
}

JPEG_QUALITY = 92  # export quality (1–95)

# ── Implementation ────────────────────────────────────────────────────────────

def _check_deps():
    missing = []
    try:
        import cv2          # noqa: F401
    except ImportError:
        missing.append("opencv-python-headless")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("pillow")
    try:
        import piexif       # noqa: F401
    except ImportError:
        missing.append("piexif")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)


def contains_face(path: Path, threshold: float = 0.5) -> bool:
    """Return True if the image appears to contain a human face."""
    import cv2
    import numpy as np

    img = cv2.imread(str(path))
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the built-in Haar cascade — no extra model files needed
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    return len(faces) > 0


def strip_gps(src_path: Path) -> bytes:
    """Return EXIF bytes with GPS IFD removed; empty bytes if no EXIF."""
    import piexif

    try:
        exif = piexif.load(str(src_path))
        exif["GPS"] = {}
        return piexif.dump(exif)
    except Exception:
        return b""


def enhance(img, preset: dict):
    """Apply PIL enhancement to an image and return the result."""
    from PIL import ImageEnhance

    img = ImageEnhance.Contrast(img).enhance(preset["contrast"])
    img = ImageEnhance.Color(img).enhance(preset["color"])
    img = ImageEnhance.Sharpness(img).enhance(preset["sharpness"])
    img = ImageEnhance.Brightness(img).enhance(preset["brightness"])
    return img


def process_photo(
    src: Path,
    out_dir: Path,
    preset: dict,
    skip_faces: bool = True,
) -> dict:
    """
    Process a single photo.

    Returns a dict:
        {"file": str, "status": "ok"|"skipped_face"|"error", "out": str|None}
    """
    from PIL import Image

    result = {"file": src.name, "out": None}

    # Face check
    if skip_faces and FACE_THRESHOLD is not None:
        try:
            if contains_face(src, FACE_THRESHOLD):
                result["status"] = "skipped_face"
                return result
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"face-check failed: {e}"
            return result

    # Open image
    try:
        img = Image.open(src).convert("RGB")
    except Exception as e:
        result["status"] = "error"
        result["error"] = f"cannot open: {e}"
        return result

    # Strip GPS
    exif_bytes = strip_gps(src)

    # Enhance
    img = enhance(img, preset)

    # Save
    out_path = out_dir / src.stem
    ext = src.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        save_path = out_dir / (src.stem + ".jpg")
        save_kwargs = {"format": "JPEG", "quality": JPEG_QUALITY}
        if exif_bytes:
            save_kwargs["exif"] = exif_bytes
        img.save(save_path, **save_kwargs)
    else:
        save_path = out_dir / (src.stem + ".png")
        img.save(save_path, format="PNG")

    result["status"] = "ok"
    result["out"] = str(save_path)
    return result


def run(photos_dir: Path, out_dir: Path, preset_name: str):
    _check_deps()

    preset = PRESETS[preset_name]
    out_dir.mkdir(parents=True, exist_ok=True)

    sources = sorted(
        f for f in photos_dir.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    )

    if not sources:
        print(f"No images found in {photos_dir}")
        sys.exit(0)

    print(f"Processing {len(sources)} image(s) with preset '{preset_name}' → {out_dir}\n")

    ok = skipped = errors = 0
    for src in sources:
        r = process_photo(src, out_dir, preset)
        status = r["status"]
        if status == "ok":
            ok += 1
            print(f"  ✅ {r['file']} → {Path(r['out']).name}")
        elif status == "skipped_face":
            skipped += 1
            print(f"  🚫 {r['file']} — face detected, excluded")
        else:
            errors += 1
            print(f"  ❌ {r['file']} — {r.get('error', 'unknown error')}")

    print(f"\nDone. {ok} exported · {skipped} excluded (faces) · {errors} errors")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Enhance photos for contest submission, strip GPS, exclude faces."
    )
    parser.add_argument(
        "--enhance",
        choices=list(PRESETS.keys()),
        default="light",
        help="Enhancement preset (default: light)",
    )
    parser.add_argument(
        "--photos",
        type=Path,
        default=PHOTOS_DIR,
        help=f"Source photo folder (default: {PHOTOS_DIR})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output folder (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--no-face-filter",
        action="store_true",
        help="Skip face detection (process all photos)",
    )
    args = parser.parse_args()

    global FACE_THRESHOLD
    if args.no_face_filter:
        FACE_THRESHOLD = None

    run(args.photos, args.out, args.enhance)


if __name__ == "__main__":
    main()
