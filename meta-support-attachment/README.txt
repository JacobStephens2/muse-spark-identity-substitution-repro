Muse Spark 1.1 identity-substitution support packet
Prepared for Meta support (Melissa); contents current as of 2026-07-31

Contents
--------
b2-opencode-write-only.json
  Exact B2 request body (OpenCode-style system prompt, write tool only).
  Request SHA-256: dfa2912b6184db146ffa07c06ddadffd12317736cf383f42450310fb3b5cf8f9

b12-minimal-neutral.json
  Exact B12 request body (minimal neutral system prompt).
  Request SHA-256: a85fcdf143515a2f4d18d113a43cf38c831261fe833dbcad4585e764b0c55570

fresh-summary-2026-07-31.json
  Committed-runner summary from the latest API-replay retest (2026-07-31 UTC).
  B2: 10/10 wrong filenames (all claude-smoke.txt)
  B12: 6/10 claude-smoke.txt, 4/10 muse-smoke.txt exact
  Response IDs for these trials live in the private repo results jsonl
  (results/2026-07-31/*.fresh.jsonl), not in this zip.

opencode-live-summary-2026-07-31.json
  Live OpenCode 1.18.5 harness summary (same day).
  10/10 wrong basenames (9 claude-smoke.txt, 1 opencode-smoke.txt).
  Tools executed under --auto in disposable dirs.
  No Meta resp_… IDs (harness session/tool ids only).

fresh-summary-2026-07-30.json
  Prior same-week API-replay retest.
  B2: 10/10 wrong filenames (all claude-smoke.txt)
  B12: 4/10 claude-smoke.txt, 6/10 muse-smoke.txt exact

opencode-live-summary-2026-07-30.json
  Prior live OpenCode summary: 10/10 claude-smoke.txt.

fresh-summary-2026-07-23.json
  Prior committed-runner summary.
  B2: 10/10 wrong filenames (9 claude-smoke.txt, 1 opencode-smoke.txt)
  B12: 3/10 claude-smoke.txt, 7/10 muse-smoke.txt exact

fresh-summary-2026-07-17.json
  Earlier committed-runner summary for comparison.
  B2: 10/10 claude-smoke.txt
  B12: 5/10 claude-smoke.txt, 5/10 muse-smoke.txt exact

REPORT.md
  Vendor-facing write-up (synced with repo REPORT.md as of 2026-07-31).

Notes
-----
- No API keys or authorization headers are included.
- This zip omits raw response ID tables; those can be sent separately or via the
  private repro repo (see meta-reply-to-melissa-response-ids.md in the repo).
- Fixed-envelope API-replay tool calls were inspected only; none were executed.
- Live OpenCode summary reflects real writes in disposable trial workspaces.
- Full trial records, runners (reproduce.py, opencode_live.py), and
  CURRENT-EVIDENCE.md live in the private reproduction repo.
  Happy to grant read-only access if useful.
