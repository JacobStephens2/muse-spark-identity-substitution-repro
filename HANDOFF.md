# Handoff: muse-spark-identity-substitution-repro

**Written:** 2026-07-31  
**Workspace:** `/Users/jacob/GitHub/JacobStephens2/muse-spark-identity-substitution-repro`  
**Branch:** `fresh-evidence-2026-07-17`  
**Purpose of next session:** Continue from here without re-deriving context. Prefer reading repo artifacts over this file for facts/rates/IDs.

---

## One-line state

**1.1** failed multi-channel through **2026-07-31** (B2/live 100% wrong). Melissa package **sent 2026-07-31 ~11:46** (rates + `resp_…` IDs + factory-seat impact). **1.2** retest **2026-08-05**: B2/B12/live all **0/10** wrong. Publication: handoff done; fair window short of full 1–2 weeks — see `PUBLICATION-DECISION.md`.

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

1. ~~**Send** Melissa reply~~ — **done 2026-07-31 ~11:46** (rates + response IDs).
2. **Publication:** near-ready for “1.1 broken / 1.2 clear” post; prefer ~**2026-08-07+** fair window, ToS check, scrub — `PUBLICATION-DECISION.md`.
3. Optional: short Melissa follow-up with 1.2 0/30 retest (close loop) before or with the post.
4. Do **not** claim live OpenCode produced Meta response IDs; do **not** claim Meta closed the ticket solely because 1.2 is clear unless they said so.

---

## 2026-07-31 rates (quick)

| Channel | Wrong rate |
|---|---:|
| B2 API | 10/10 |
| B12 API | 6/10 |
| Live OpenCode | 10/10 |

Factory-seat decision: **still no**.
