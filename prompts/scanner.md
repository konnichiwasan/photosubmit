# photosubmit — Daily Scanner Prompt

Paste this into Claude (or any capable LLM with web access) for each scan run.
Before pasting, replace `[PORTFOLIO]` with the contents of your `my-portfolio.md`.
Save the output as `scan-YYYY-MM-DD.md` in your scans folder.

---

You are running a daily photo contest scan. Your job is to find free photo contests,
verify they are genuinely free, check fit against my portfolio, and update the shortlist.

## My portfolio

[PORTFOLIO]

## Shortlist (current)

[paste contents of shortlist.md here, or write "empty" if first run]

## Instructions

**Step 1 — Scan sources**

Check all of the following for new free contests:
- https://www.photocontestguru.com/free-photo-contest-list/
- https://www.photocontestguru.com (closing-soon section)
- https://www.deartline.com/photo-contests/free-photo-contests/
- Web search: `free photo contests [current year] open submissions`

**Step 2 — Verify each candidate**

For every contest that looks free, verify:
- [ ] Entry fee: Free (no fee at any tier)
- [ ] Membership: Not required (or free membership available)
- [ ] Rights: Photographer retains copyright (flag if exclusive rights clause)
- [ ] Deadline: Still open

Exclude anything that fails any of the above. Note the reason.

**Step 3 — Check fit**

For contests that pass verification, check which of my ready photos fit best.
Consider: theme match, genre match, edit restrictions, submission limits.

**Step 4 — Write the scan report**

Use this structure:

```
# Daily Photo Contest Scan — [DATE]

*Sources checked: [list]*

## Summary
[1–2 lines: how many new contests found, added, excluded]

## New verified-free contests

### [Contest name] · [URL]
- Deadline: 
- Fee: Free (verified via [source])
- Theme: 
- Specs: 
- Edit restrictions: 
- Fit: [which of my photos, and why]
- Action: [what I need to do]

## Excluded today
| Contest | Reason |
|---|---|

## Deadline countdown — all open contests
| Contest | Deadline | Days left | Lead photo |
|---|---|---|---|

## Named targets status
[Check on any major annual contests not yet open — Smithsonian, Sony, HIPA, etc.]
```

**Rules:**
- Never add a contest without verifying the fee directly on its official page or a trusted aggregator (photocontestguru, deartline).
- Flag any contest with an exclusive rights clause even if it is otherwise free.
- Do not submit on my behalf. End the report with any actions I need to take myself.
