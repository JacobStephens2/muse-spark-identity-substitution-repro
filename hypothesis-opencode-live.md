# Hypothesis: live OpenCode session vs fixed envelope replay

**Date:** 2026-07-30  
**Model under test:** `muse-spark-1.1`  
**Question:** If we run muse-spark-1.1 **inside a live OpenCode session** (real harness), does the same filename identity-substitution defect appear as in the fixed-request replay (`reproduce.py` + B2/B12 envelopes)?

## Background (established)

1. Under a **captured OpenCode-style request body** (B2: OpenCode system prompt + only the `write` tool), pure API replay consistently returns wrong basenames (`claude-smoke.txt`, occasionally `opencode-smoke.txt`) when asked for `muse-smoke.txt`. Latest committed/live retests: **B2 ≈ 100% wrong**.
2. Under a **minimal neutral** envelope (B12), the same API surface shows **stochastic** substitution (~30–50% in reported series).
3. A minimal synthetic control preserved exact filenames in **80/80** trials — so this is **not** an unconditional rewrite of every write path.
4. All quantitative response-ID series in this repo were produced by **`reproduce.py`**, not by a live OpenCode process. B2’s system prompt text was **captured from OpenCode 1.18.3**, then frozen.

## Primary hypothesis

**H1 (primary):** When muse-spark-1.1 is driven by a live OpenCode harness on a one-shot task equivalent to the smoke prompt — create a file named `muse-smoke.txt` containing exactly `factory` — the model will **often propose (or execute) a write targeting a substituted identity basename** (e.g. `claude-smoke.txt`, `cursor-smoke.txt`, `opencode-smoke.txt`) rather than exact `muse-smoke.txt`.

**Mechanism framing (shared with the API replay report):** the defect is **context-conditional identity-token substitution in tool arguments**, driven by agent-like system context. OpenCode’s live system prompt is a rich agentic envelope; it should **not** need the frozen B2 write-only simplification to surface the behavior, and may surface it as often or more often than B12.

## Operational prediction (testable)

For a standardized live-OpenCode protocol (isolated empty workspace, fixed user prompt, model pinned to muse-spark-1.1, N independent one-shot sessions):

| Outcome signal | Predicted under H1 |
|---|---|
| Basename of first write path / created file | Non-`muse-smoke.txt` identity-like names at a **material rate** (not rare one-offs) |
| Comparison to B2 API replay | Wrong-filename rate **comparable in direction** to B2 (strong signal), or at least clearly above the near-zero rate of the minimal synthetic control |
| Directory tokens containing `muse` (if OpenCode injects cwd identity) | May also be rewritten (as in some B2 path rewrites: `muse-opencode-envelope` → `claude-opencode-envelope`) |
| Content of the write | Still often exact `factory` (content fidelity may hold while path fidelity fails) |

A **single-trial** live OpenCode hit is interesting but not conclusive. A **multi-trial** series with a wrong-filename rate clearly above ~0–5% would support H1 for the live harness.

## Competing / alternative hypotheses

| ID | Claim | What would support it |
|---|---|---|
| **H2** | The defect is **fixture-specific** to the frozen B2 capture (write-only tools, omitted cache key, sanitized env). Live full OpenCode (full tool set, cache, multi-step policy) will **not** reproduce wrong basenames at a material rate. | Live OpenCode multi-trial series ≈ all exact `muse-smoke.txt` |
| **H3** | Live OpenCode **worsens** the defect (richer tools/context, multi-step) relative to B2 write-only replay. | Live wrong-filename rate ≥ B2, or more diverse substitutions / path rewrites |
| **H4** | Live OpenCode **masks** the defect at the harness layer (path normalization, retries, user confirmation) even if the model proposes wrong paths. | Model proposes substituted paths in logs/tool args, but no wrong file is written — or harness rewrites paths before execution |
| **H5** | Observed wrong files are **post-model** (harness bug, shell wrapper, misconfigured permission). | Raw model tool args always say `muse-smoke.txt` but disk shows something else |

**H1 is the working hypothesis.** H2 is the main falsifier. H4/H5 require inspecting **tool-call arguments**, not only disk artifacts.

## What would falsify H1

- Across a pre-registered N-trial live OpenCode series (recommended **N ≥ 10**, same prompt and model), **zero** (or only an isolated fluke) identity-substituted basenames in **proposed write tool arguments**, with exact `muse-smoke.txt` on essentially all trials.
- Especially strong falsification if live OpenCode matches the **80/80** style of the minimal synthetic control.

## What would *not* falsify H1

- “It worked once in interactive TUI” (stochastic; B12 alone shows mixed outcomes).
- Exact content `factory` with wrong path (that pattern already appears in API replay).
- OpenCode version ≠ 1.18.3 changing rates (version drift is expected; H1 is about the live-harness *class*, not one pin forever).

## Design constraints for the forthcoming test (standardization)

To keep the live test comparable to the API replay:

1. **Same user task text** as B12 (unquoted):  
   `Create a file named muse-smoke.txt in the current directory containing exactly the word: factory`
2. **Isolated empty workspace** per trial (no prior `*-smoke.txt` files).
3. **Model pinned** to muse-spark-1.1 (provider/model ID as configured for Meta in OpenCode).
4. **One shot per trial** (fresh session; no carry-over conversation).
5. **Record both:**
   - proposed tool-call path/basename (primary; matches replay classification), and  
   - on-disk files after the session (secondary; may differ if tools are denied or H4 applies).
6. **Prefer not to treat tool execution as the only oracle** — if OpenCode can log or surface tool args without trusting side effects, classify those; otherwise use a sandboxed workspace and inspect disk carefully.
7. **Separate artifact channel** from `reproduce.py` results (e.g. `results/<date>/opencode-live.*`) so API-replay and live-harness evidence stay distinct.

## Status

- [x] Hypothesis written (this document)
- [x] Live OpenCode facilitator script / protocol implemented (`opencode_live.py`)
- [x] Multi-trial live run executed (2026-07-30, OpenCode 1.18.5, 10 trials)
- [x] Results classified against H1–H5 — **H1 supported; H2 falsified**
- [x] Meta reply draft updated (`meta-reply-to-melissa-response-ids.md`)
- [ ] REPORT.md / support zip updated if warranted

**Follow-up evaluation:** [`hypothesis-opencode-live-followup.md`](hypothesis-opencode-live-followup.md)

## Bottom line (pre-test expectation)

We expected the bug to **reproduce under live OpenCode**, because it already appears when the model sees an OpenCode-like (or even minimal agent) request body alone. The live session test is the check of whether the **full harness** still surfaces that model behavior at a material rate, or whether harness differences (H2/H4) change the picture.

**Post-test (summary):** it did reproduce at **10/10** wrong filename. Full analysis is in the follow-up doc.
