# photosubmit — Onboarding Prompt

Paste this into Claude (or any capable LLM with web access) once, at the start.
Save the output as `my-portfolio.md` next to this file. The scanner prompt reads it.

---

I am setting up a photo contest tracking system. Help me build my portfolio profile.

Ask me the following, one at a time, and wait for my answers:

1. **My photos** — What photos do I have ready to submit? For each, give me a short slug name (e.g. `mineral_lake_storm_sky`) and a one-sentence description of what's in it.

2. **Genres** — What genres do these photos fall into? (landscape, nature, macro, wildlife, street, portrait, travel, abstract, weather, etc.)

3. **Edit restrictions** — Have any of these photos been heavily composited or AI-edited? (Some contests prohibit this — I need to know which photos to flag.)

4. **Contest priorities** — What matters most to me in a contest? Rank: prize money / prestige / publication / international reach / deadline proximity.

5. **Hard exclusions** — Anything I will never enter? (e.g. contests requiring model releases, contests with exclusive rights clauses, contests in specific countries)

Once I've answered, write a `my-portfolio.md` file in this format:

```
# My Portfolio

## Ready photos
- slug: description

## Genres
...

## Edit notes
...

## Contest priorities
...

## Hard exclusions
...
```

This file is the scanner's starting context. Keep it factual and short — one line per item.
