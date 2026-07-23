Muse Spark 1.1 identity-substitution support packet
Prepared for Meta support (Melissa), 2026-07-23

Contents
--------
b2-opencode-write-only.json
  Exact B2 request body (OpenCode-style system prompt, write tool only).
  Request SHA-256: dfa2912b6184db146ffa07c06ddadffd12317736cf383f42450310fb3b5cf8f9

b12-minimal-neutral.json
  Exact B12 request body (minimal neutral system prompt).
  Request SHA-256: a85fcdf143515a2f4d18d113a43cf38c831261fe833dbcad4585e764b0c55570

fresh-summary-2026-07-23.json
  Committed-runner summary from the latest retest (2026-07-23 UTC).
  B2: 10/10 wrong filenames (9 claude-smoke.txt, 1 opencode-smoke.txt)
  B12: 3/10 claude-smoke.txt, 7/10 muse-smoke.txt exact

fresh-summary-2026-07-17.json
  Prior committed-runner summary for comparison.
  B2: 10/10 claude-smoke.txt
  B12: 5/10 claude-smoke.txt, 5/10 muse-smoke.txt exact

REPORT.md
  Vendor-facing write-up with environment, integrity checks, and limitations.

Notes
-----
- No API keys, response IDs, or authorization headers are included.
- Returned tool calls were inspected only; none were executed.
- Full trial records and the Python runner live in the private reproduction repo.
  Happy to grant read-only access or send response IDs if useful.
