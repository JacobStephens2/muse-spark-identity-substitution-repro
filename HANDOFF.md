# Handoff: muse-spark-identity-substitution-repro

**Written:** 2026-08-05  
**Workspace:** `/Users/jacob/GitHub/JacobStephens2/muse-spark-identity-substitution-repro`  
**Branch:** `fresh-evidence-2026-07-17`  
**Purpose of next session:** Continue from here without re-deriving context. Prefer reading repo artifacts over this file for facts/rates/IDs.

---

## One-line state

**1.1** failed multi-channel through **2026-07-31** (B2/live 100% wrong). Melissa package **sent 2026-07-31 ~11:46**. **1.2** retest **2026-08-05**: B2/B12/live OpenCode all **0/10** wrong. **Muse Code** explored same day: first-party **harness** (not a new model); default **`muse-spark-1.2-contributor`**; single `hello.py` smoke succeeded with Meta `resp_…` IDs — **not** an identity-sub N=10 series. Docs: `muse-code.md`, `CURRENT-EVIDENCE.md` Channel D. Publication: fair window short of full 1–2 weeks — `PUBLICATION-DECISION.md`.

---

## Do not re-do

- Re-explaining the defect from scratch — use `CURRENT-EVIDENCE.md` and `REPORT.md`.
- Re-running large trial series unless the user asks or a serving change is suspected.
- Updating Mimestream automatically — user said **stop updating Mimestream**; edit local markdown only unless asked.
- Putting API keys, auth.json contents, Muse `~/.config/muse/auth.json`, or raw secrets in commits.
- Claiming Muse Code multi-trial identity-sub rates or that Muse Code is “better than OpenCode on 1.2” without a side-by-side series.

---

## Conversation arc (recent)

1. Melissa framed issue as tool-use fidelity; asked for **response IDs**.
2. 2026-07-30 / 07-31: 1.1 still broken multi-channel; Melissa package sent with rates + IDs.
3. 2026-08-05: **muse-spark-1.2** multi-channel retest → **0/30** wrong (B2, B12, live OpenCode).
4. 2026-08-05: Meta email announced **Muse Code** + expanded Muse Spark 1.2 access. Local tryout: install `muse`, auth, headless smoke. Confirmed **harness vs model**; compared to OpenCode; documented in `muse-code.md` + Channel D artifacts.

---

## Authoritative artifacts (read these, don’t paste)

| Path | Use |
|---|---|
| `CURRENT-EVIDENCE.md` | Multi-channel map, rates, response IDs, factory decision, Channel D pointer |
| `muse-code.md` | Muse Code = harness; smoke details; vs OpenCode comparison |
| `results/2026-08-05/muse-code/` | Smoke `summary.json`, `events.jsonl`, `hello.py` |
| `results/2026-08-05/` | **1.2** API jsonl + live OpenCode 0/10 |
| `REPORT.md` | Vendor-facing narrative (1.1-focused; 1.2 clearance in evidence map) |
| `README.md` | How to run; doc index |
| `PUBLICATION-DECISION.md` | When to publish/update a public blog post |
| `meta-reply-to-melissa-response-ids.md` | Melissa reply (2026-07-31 IDs + rates) |
| `reproduce.py` / `opencode_live.py` | Channel A / B runners |
| `THIRD_PARTY_NOTICES.md` | OpenCode fixture / live CLI notes |

---

## Operational notes

- **Credentials:** Prefer one env export — `MODEL_API_KEY` or `META_AI_API_KEY` (see `meta_auth.py`, `.env.example`). Muse Code: `muse auth set` or `META_API_KEY` / `muse login`. Do not commit keys, OpenCode `auth.json`, or Muse `auth.json`.
- **Channels:** A = fixed envelope API (`resp_…`); B = live OpenCode (no Meta `resp_…`); D = Muse Code (smoke only so far; can include `resp_…`).
- **Safety:** `reproduce.py` never executes tools. `opencode_live.py --auto` and `muse exec --disable-approval` **do** execute in their workspaces.
- **User preference:** Do not auto-update Mimestream; local markdown only unless asked.

---

## Likely next tasks (user-dependent)

1. **Publication:** “1.1 broken / 1.2 clear” post; prefer ~**2026-08-07+** fair window, ToS check, scrub — `PUBLICATION-DECISION.md`.
2. Optional: short Melissa follow-up with 1.2 0/30 retest (close loop).
3. Optional: multi-trial **Muse Code** `muse-smoke.txt` series (Channel D) if first-party harness rates are needed — do not invent rates before that.
4. Do **not** claim live OpenCode produced Meta response IDs; do **not** claim Meta closed the ticket solely because 1.2 is clear unless they said so; do **not** call Muse Code a separate model from Muse Spark 1.2.

---

## Rates (quick)

### 2026-07-31 (`muse-spark-1.1`)

| Channel | Wrong rate |
|---|---:|
| B2 API | 10/10 |
| B12 API | 6/10 |
| Live OpenCode | 10/10 |

Factory-seat decision for **1.1**: **no**.

### 2026-08-05 (`muse-spark-1.2`)

| Channel | Wrong rate |
|---|---:|
| B2 API | 0/10 |
| B12 API | 0/10 |
| Live OpenCode | 0/10 |
| Muse Code smoke | n/a (not smoke-protocol N=10) |
