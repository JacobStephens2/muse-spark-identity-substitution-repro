# Handoff: muse-spark-identity-substitution-repro

**Written:** 2026-07-31  
**Workspace:** `/Users/jacob/GitHub/JacobStephens2/muse-spark-identity-substitution-repro`  
**Branch:** `fresh-evidence-2026-07-17`  
**Purpose of next session:** Continue from here without re-deriving context. Prefer reading repo artifacts over this file for facts/rates/IDs.

---

## One-line state

Meta (`muse-spark-1.1`) still substitutes identity-like filenames in write-tool args; **2026-07-31** retests confirm no fix (B2 10/10, B12 6/10, live OpenCode 10/10 wrong). Melissa reply draft has today’s rates + response IDs and OpenCode/factory-seat impact framing. Results and docs updated for this series.

---

## Do not re-do

- Re-explaining the defect from scratch — use `CURRENT-EVIDENCE.md` and `REPORT.md`.
- Re-running large trial series unless the user asks or a serving change is suspected.
- Updating Mimestream automatically — user said **stop updating Mimestream**; edit local markdown only unless asked.
- Putting API keys, auth.json contents, or raw secrets in commits.

---

## Conversation arc (recent)

1. Melissa framed issue as tool-use fidelity; asked for **response IDs**.
2. 2026-07-30: B2 10/10, B12 4/10 API replay; live OpenCode 10/10; reply draft + support packet.
3. 2026-07-31: full retest again → B2 **10/10**, B12 **6/10**, live OpenCode **10/10** (9 claude, 1 opencode). No improvement.
4. Email impact framing: blocks reliable muse-spark-1.1 use **with OpenCode** / factory seat.
5. Docs, Melissa draft, support packet refreshed for 2026-07-31.

---

## Authoritative artifacts (read these, don’t paste)

| Path | Use |
|---|---|
| `CURRENT-EVIDENCE.md` | Multi-channel map, rates, where response IDs live, factory decision |
| `REPORT.md` | Vendor-facing narrative (updated for 2026-07-31) |
| `README.md` | How to run; doc index |
| `meta-reply-to-melissa-response-ids.md` | **Current** Melissa reply (2026-07-31 IDs + rates) |
| `PUBLICATION-DECISION.md` | When to publish/update a public blog post |
| `meta-reply-to-melissa-warmer.md` / `meta-reply-to-melissa.txt` | Historical only (superseded banners) |
| `hypothesis-opencode-live.md` | Pre-registered H1–H5 |
| `hypothesis-opencode-live-followup.md` | Evaluation after 2026-07-30 live run |
| `reproduce.py` | Fixed envelope API replay (no tool execution) |
| `opencode_live.py` + `opencode-live/` | Live OpenCode facilitator |
| `results/2026-07-31/` | **Latest** API jsonl (with `response_id`) + `opencode-live/` |
| `results/2026-07-30/` | Prior same-week series |
| `meta-support-attachment/` + `meta-support-attachment.zip` | Support packet (summaries, no raw resp ID tables) |
| `THIRD_PARTY_NOTICES.md` | OpenCode fixture / live CLI notes |

---

## Operational notes

- **Credentials:** Prefer one env export — `MODEL_API_KEY` or `META_AI_API_KEY` (see `meta_auth.py`, `.env.example`). `reproduce.py` accepts either; optional `--from-opencode-auth` / `MUSE_ALLOW_OPENCODE_AUTH=1` falls back to OpenCode `auth.json`. `opencode_live.py` seeds OpenCode `meta` from env only if missing (never overwrites). Do not commit keys or `auth.json`.
- **Channel A vs B:** Only Channel A yields Meta `resp_…` IDs. Live OpenCode has `ses_…` / tool `call_…` only.
- **Safety:** `reproduce.py` never executes tools. `opencode_live.py --auto` **does** execute writes in trial dirs; absolute path rewrites can escape the workspace.
- **User preference:** Do not auto-update Mimestream; local markdown only unless asked.
- **Melissa’s open ask:** Provide response IDs (in draft for 2026-07-31); engineering investigation pending. User may still need to **send** the reply manually.

---

## Likely next tasks (user-dependent)

1. **Send** Melissa reply (user; not agent) — draft: `meta-reply-to-melissa-response-ids.md`.
2. **Publication:** do **not** blog yet; criteria and update rules in `PUBLICATION-DECISION.md`.
3. Optional: further experiments in `hypothesis-opencode-live-followup.md` §9 (only if asked).
4. Do **not** claim live OpenCode produced Meta response IDs.

---

## 2026-07-31 rates (quick)

| Channel | Wrong rate |
|---|---:|
| B2 API | 10/10 |
| B12 API | 6/10 |
| Live OpenCode | 10/10 |

Factory-seat decision: **still no**.
