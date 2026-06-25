# photosubmit

A two-stage photo contest pipeline: find free contests, then prepare your photos for submission.

```
   prompts/onboarding.md
          │
          ▼ (run once)
     my-portfolio.md ── your photos, genres, priorities
          │
          ▼ (run daily or weekly)
   prompts/scanner.md ── LLM searches contest sources, verifies fees
          │
          ▼
     scan-YYYY-MM-DD.md ── new contests, deadline countdown, photo fit
          │
          ▼
     shortlist.md ── verified free contests with deadlines + fit notes
          │
          ▼ (you pick a contest)
   contest_pipeline.py
          │
        ┌─┴──────────────────────┐
        ▼                        ▼
  face detection            strip GPS
  (skip if found)           from EXIF
        │                        │
        └──────────┬─────────────┘
                   ▼
          apply enhancement preset
                   │
                   ▼
          submission_ready/
```

## Why this exists

Finding free photo contests is slow. Verifying they're actually free — not "free tier" with a paid upgrade, not "free entry" with a mandatory rights transfer — takes longer. And once you've found one, preparing your photos consistently (same enhancement pass, GPS stripped, faces excluded) takes another round of manual work.

`photosubmit` handles both halves. The scanner is a prompt you paste into an LLM; it searches the main aggregators, verifies fee status directly on each contest's page, and tells you which of your photos fits which contest. The pipeline script takes it from there: face detection, GPS strip, enhancement, clean export.

No SaaS. No account. Your photos and your shortlist stay local.

## What you get

- **`prompts/onboarding.md`** — run once to build your portfolio profile
- **`prompts/scanner.md`** — run daily or weekly; paste into Claude or any LLM with web access
- **`contest_pipeline.py`** — processes photos: excludes faces, strips GPS, applies enhancement preset, exports to `submission_ready/`
- **`templates/`** — blank shortlist and submission package templates to track your open contests

## Quickstart

**1. Onboard**

Paste `prompts/onboarding.md` into an LLM. Answer its questions about your photos, genres, and preferences. Save the output as `my-portfolio.md`.

**2. Scan**

Paste `prompts/scanner.md` into an LLM (with web access). Replace `[PORTFOLIO]` with your `my-portfolio.md` contents. The LLM searches photocontestguru.com, deartline.com, and the web; verifies fees; checks photo fit. Save the output as `scan-YYYY-MM-DD.md`.

**3. Update your shortlist**

Copy verified contests into `shortlist.md`. Use `templates/shortlist.md` as the starting point.

**4. Prepare your photos**

```bash
pip install opencv-python-headless pillow piexif

# Light enhancement (default — for contests requiring minimal processing)
python3 contest_pipeline.py

# Strong enhancement (punchy contrast/colour for nature/landscape)
python3 contest_pipeline.py --enhance strong

# Custom folders
python3 contest_pipeline.py --photos ~/Desktop/shots --out ~/Desktop/ready

# Skip face detection
python3 contest_pipeline.py --no-face-filter
```

Drop source photos into a `photos/` folder next to the script. Processed exports go to `submission_ready/`, originals untouched.

**5. Track submissions**

Copy `templates/submission_packages.md` and fill in one block per contest entry before you submit.

## Pipeline configuration

Edit the constants at the top of `contest_pipeline.py`:

```python
PHOTOS_DIR     = Path(__file__).parent / "photos"
DEFAULT_OUT    = Path(__file__).parent / "submission_ready"
FACE_THRESHOLD = 0.5   # 0–1, higher = stricter; None = disabled
JPEG_QUALITY   = 92
```

Enhancement presets are in the `PRESETS` dict — tweak contrast, color, sharpness, and brightness to taste.

## Design decisions

- **Scanner is LLM-driven, not scraped.** Contest sites change structure constantly. An LLM that reads the actual page and reasons about fee status is more reliable than a scraper that breaks on every redesign.
- **Free means free.** The scanner prompt instructs the LLM to check for entry fees, mandatory paid membership, and exclusive rights clauses — all three. A contest that fails any one is excluded.
- **Face detection is on by default.** Most open contests prohibit identifiable people. Pass `--no-face-filter` to skip it.
- **GPS stripping is always on.** No flag to keep it. If a contest requires location metadata, submit from your original manually.
- **Originals are never modified.** The pipeline writes to a separate output folder.

## Project layout

```
photosubmit/
├── README.md
├── .env.example
├── contest_pipeline.py
├── prompts/
│   ├── onboarding.md       run once — builds your portfolio profile
│   └── scanner.md          run daily/weekly — finds and verifies free contests
└── templates/
    ├── shortlist.md        track verified open contests
    └── submission_packages.md   track per-contest submission status
```

## Status

Working. The scanner prompt is tuned for photocontestguru.com and deartline.com — the two most reliable free-contest aggregators. If you find a better source, add it to the Sources section at the top of `prompts/scanner.md`. Issues and PRs welcome.

## License

MIT.
