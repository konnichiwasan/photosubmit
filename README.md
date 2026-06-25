# photosubmit

A photo contest submission pipeline that filters, enhances, and scrubs your images before they go out.

```
       your photos folder
              │
              ▼
       face detection ──── face found? ──── skip
              │
              ▼ (no face)
       strip GPS metadata
              │
              ▼
       apply enhancement preset
              │
              ▼
       submission_ready/
```

## Why this exists

Most photo contests have quiet rules: no identifiable people, no embedded location data, images processed but not over-processed. Doing this manually — opening each photo, checking for faces, pulling EXIF, running an edit, exporting — is tedious enough that corners get cut.

`photosubmit` runs the whole chain in one command. It excludes images with faces automatically, strips GPS from EXIF so you're not revealing where you shoot, and applies a named enhancement preset so your edits are consistent across a batch rather than eyeballed one at a time.

No cloud, no account, no upload. Your photos stay local.

## What you get

- Face detection via OpenCV's Haar cascade — no model downloads, no API
- GPS stripping from EXIF on export
- Two enhancement presets (`strong` for nature/landscape contests, `light` for minimal-processing rules)
- Clean exports to a `submission_ready/` folder, originals untouched

## Quickstart

```bash
pip install opencv-python-headless pillow piexif
```

Drop your source photos into a `photos/` folder next to the script, then:

```bash
# Light enhancement (default)
python3 contest_pipeline.py

# Strong enhancement
python3 contest_pipeline.py --enhance strong

# Skip face detection entirely
python3 contest_pipeline.py --no-face-filter

# Custom folders
python3 contest_pipeline.py --photos ~/Desktop/shots --out ~/Desktop/ready
```

The script prints a per-image status line — ✅ exported, 🚫 face detected, ❌ error — and a summary count at the end.

## Configuration

Edit the constants at the top of `contest_pipeline.py`:

```python
PHOTOS_DIR      = Path(__file__).parent / "photos"            # source folder
DEFAULT_OUT     = Path(__file__).parent / "submission_ready"  # output folder
FACE_THRESHOLD  = 0.5    # 0–1, higher = stricter; None = disabled
JPEG_QUALITY    = 92     # export quality
```

Enhancement presets live in the `PRESETS` dict — tweak the contrast, color, sharpness, and brightness multipliers to taste.

## Design decisions

- **Face detection is on by default.** Most open contests prohibit identifiable people. Opt out with `--no-face-filter` if your contest is a portrait category or you've already curated the folder.
- **GPS stripping is always on.** There's no flag to keep it. If a contest requires location metadata, export from your original and submit manually — that's the exception, not the rule.
- **Originals are never modified.** The script reads from your source folder and writes to a separate output folder. Running it twice is safe.
- **No cloud dependencies.** Face detection uses OpenCV's built-in Haar cascade. No API key, no model file to download, no call home.

## Project layout

```
photosubmit/
├── README.md
├── .env.example          copy to .env and fill in your details
└── contest_pipeline.py   the pipeline
```

## Status

Working and minimal. The enhancement presets are tuned for nature and landscape work — if you shoot in a different genre, the multipliers in `PRESETS` are the place to start. Issues and PRs welcome.

## License

MIT.
