# Follow-up: live OpenCode hypothesis evaluation

**Date:** 2026-07-30  
**Parent document:** [`hypothesis-opencode-live.md`](hypothesis-opencode-live.md)  
**Model:** `muse-spark-1.1` (OpenCode id `meta/muse-spark-1.1`)  
**Question under test:** Does identity substitution of user-supplied write paths reproduce under a **live OpenCode harness**, not only under fixed envelope API replay?

## 1. Verdict (executive)

| Hypothesis | Verdict |
|---|---|
| **H1** (live OpenCode often substitutes identity-like basenames) | **Supported** |
| **H2** (fixture-only / live OpenCode will not reproduce) | **Falsified** |
| **H3** (live harness worsens vs B2) | **Compatible, not required** — rate matches B2 (100%), not higher |
| **H4** (harness masks wrong model paths) | **Not supported** on this series |
| **H5** (wrong files are post-model only) | **Not supported** on this series |

**Bottom line:** On a pre-registered 10-trial live OpenCode protocol, muse-spark-1.1 produced **0** exact `muse-smoke.txt` writes and **10/10** `claude-smoke.txt` substitutions. The defect is therefore **not limited** to the frozen B2 write-only request body; it appears in the full agent harness used for coding-agent evaluation.

## 2. Link back to the registered prediction

From the parent hypothesis, H1 predicted a **material** wrong-filename rate under live OpenCode for the smoke task, comparable in direction to B2 API replay (strong signal), with content often still `factory`, and possible directory-token rewrites.

**Observed:** 100% wrong basename, content `factory`, at least one directory/path-token rewrite — matches the operational prediction and exceeds the “material rate” bar by a wide margin.

**Falsification criteria for H1 were not met:** there was no near-perfect exact-basename series, and no 80/80-style control outcome.

## 3. Method actually used

Facilitator: [`opencode_live.py`](opencode_live.py)  
Harness config: [`opencode-live/`](opencode-live/)  
Protocol alignment with parent design constraints:

| Constraint | Implementation |
|---|---|
| Same user task as B12 | Exact B12 text: create `muse-smoke.txt` with content `factory` |
| Isolated empty workspace | `results/2026-07-30/opencode-live/trial-NN/` per trial |
| Model pin | `meta/muse-spark-1.1` |
| One shot / no carry-over | Fresh `opencode run` session per trial |
| Primary oracle | First `write` tool `filePath` in `--format json` event stream |
| Secondary oracle | On-disk `*smoke*.txt` after session |
| Separate from API replay | Artifacts under `results/2026-07-30/opencode-live/`, not `reproduce.py` jsonl |

Additional run parameters:

- OpenCode version: **1.18.5** (original B2 capture class was 1.18.3)
- Provider: Meta Model API (`baseURL` `https://api.meta.ai/v1`, `@ai-sdk/openai` adapter)
- Permissions: `--auto` (non-interactive completion; tools executed in trial workspaces)
- Trials: **N = 10** (parent recommended N ≥ 10)

## 4. Results

Machine-readable summary: [`results/2026-07-30/opencode-live/summary.json`](results/2026-07-30/opencode-live/summary.json)  
Per-trial records: [`results/2026-07-30/opencode-live/trials.jsonl`](results/2026-07-30/opencode-live/trials.jsonl)

| Trial | Classification | First write basename | Oracle | Notes |
|---:|---|---|---|---|
| 1 | `claude_substitution` | `claude-smoke.txt` | tool arg | content `factory` |
| 2 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 3 | `claude_substitution` | `claude-smoke.txt` | tool arg | also rewrote a parent path segment `muse-spark-…` → `claude-…` |
| 4 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 5 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 6 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 7 | `claude_substitution` | (disk) `claude-smoke.txt` | disk | write event missing from captured stream; file present |
| 8 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 9 | `claude_substitution` | `claude-smoke.txt` | tool arg | |
| 10 | `claude_substitution` | `claude-smoke.txt` | tool arg | |

| Aggregate | Value |
|---|---|
| Trials completed | 10/10 |
| Wrong-filename rate | **1.0** (10/10) |
| Exact `muse-smoke.txt` | **0** |
| Alternate identity basenames seen | `claude-smoke.txt` only (this series) |
| Content fidelity | `factory` on observed writes |

Same-day API-replay comparison (for context only; separate method):

| Channel | Wrong-filename rate (2026-07-30) |
|---|---|
| B2 fixed envelope (`reproduce.py`) | 10/10 (100%) |
| B12 fixed envelope (`reproduce.py`) | 4/10 (40%) |
| Live OpenCode (`opencode_live.py`) | 10/10 (100%) |

## 5. Evaluation of each hypothesis

### H1 — Supported

Live OpenCode produced identity-substituted write targets on **all** trials. That is stronger than “material rate” and is **not** a one-off interactive fluke. Tool-arg paths (primary oracle) show the model proposed `claude-smoke.txt`; disk confirms execution of that wrong path under `--auto`.

### H2 — Falsified

H2 claimed the defect was specific to the frozen B2 capture (write-only tools, omitted cache key, sanitized env). Live full OpenCode used the normal agent tool surface and still hit **100%** wrong basename. The defect generalizes at least to this live-harness class.

### H3 — Compatible, not established as “worse than B2”

Live rate equals latest B2 rate (100%), so live did not need to be *worse* than B2 to matter. This series did not show a *higher* rate than B2 (ceiling effect). Path diversity beyond basename was limited but non-zero (trial 3 directory-token rewrite). Treat H3 as open if future runs show more multi-step damage or more identity targets; not required for the main claim.

### H4 — Not supported

Harness masking would look like: model says `claude-…`, disk ends as `muse-…`, or no write lands. Observed pattern: model path and disk basename agree on `claude-smoke.txt` (except trial 7, where only disk was captured — still wrong). Auto-approval **executed** the bad path rather than blocking it.

### H5 — Not supported

Post-model-only failure would look like: tool args always `muse-smoke.txt` while disk differs. Observed: tool args themselves carry `claude-smoke.txt` on 9/10 captured write events.

## 6. Interpretation

1. **Channel independence:** The same user-visible failure mode appears in (a) fixed OpenCode-style envelope replay, (b) minimal neutral envelope (stochastically), and (c) live OpenCode. That strengthens the claim that the behavior is model/serving-side under agentic context, not an artifact of a single hand-frozen JSON file alone.
2. **Impact for coding-agent use:** In live OpenCode with tool execution enabled, wrong paths are not merely theoretical tool-arg noise — they become real files. That matches the software-factory reliability gate: exact path fidelity is a hard prerequisite and is not met.
3. **Content vs path asymmetry (still present):** Content remained `factory` while the basename changed. Path/identity tokens appear more fragile than literal content in this smoke task.
4. **Directory tokens remain fragile:** Trial 3’s parent-path rewrite echoes B2 API-replay rewrites of `muse-opencode-envelope` → `claude-opencode-envelope`. Identity-like path components can be rewritten, not only basenames.
5. **What this does *not* prove:** Root cause (training, distillation, alignment, serving). It also does not measure rates under other harnesses (Cursor, Codex, Claude Code, custom factory runners) or under multi-file agent tasks.

## 7. Limitations

- N = 10 is enough to reject “essentially never happens” for this protocol, but Wilson-style uncertainty still exists for fine-grained rate estimates (here the point estimate is at the ceiling).
- OpenCode **1.18.5** ≠ capture version **1.18.3**; H1 was about harness *class*, not a permanent pin.
- `--auto` executes tools; production policy may differ, but proposed tool args already fail fidelity before policy.
- Trial 7 lacked a captured write event; classification relied on disk. Overall conclusion does not depend on that single trial.
- Live harness does not expose Meta `resp_…` IDs the same way as `reproduce.py`; correlation to serving revision still relies on the API-replay response-ID series.
- Accidental out-of-workspace writes are possible when the model rewrites absolute path prefixes (observed once); workspaces should remain disposable.

## 8. Implications for the Meta report

- **Reliability framing remains correct:** tool-argument fidelity defect with agent impact.
- **Add live-harness evidence** alongside fixed envelopes: not only B2/B12 hashes, but “full OpenCode one-shot, 10/10 wrong basename.”
- **Response IDs** remain the best internal tracing handle for engineering; live sessions supplement with session/tool call IDs and jsonl if needed.
- **Product decision (local):** muse-spark-1.1 still fails the software-factory coding-agent reliability pre-check.

Draft email text incorporates this channel in [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md). [`REPORT.md`](REPORT.md) and [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) include the live series; the Meta support zip has been refreshed with 2026-07-30 summaries.

## 9. Next experiments (optional)

| Priority | Experiment | Why |
|---|---|---|
| P1 | Pin OpenCode version and re-run after any Meta serving change | Detect fix vs regression |
| P2 | Live OpenCode with tool execution denied / ask-only; classify tool args only | Safer oracle, closer to “inspect not execute” |
| P3 | Other identity-like names (`acme-smoke.txt`, UUID basenames, no identity prefix) | Bound how identity-like the trigger is under the full harness |
| P4 | Multi-file / edit-existing-file tasks | Factory-like workload, not only create-new |
| P5 | Update `REPORT.md` + support zip with live summary | Vendor packet completeness |

## 10. Repro command

```bash
# Requires OpenCode + Meta provider credentials configured
python3 opencode_live.py --trials 10 --model meta/muse-spark-1.1
```

Outputs land in `results/<UTC-date>/opencode-live/`.

## 11. Status relative to parent checklist

| Item | Status |
|---|---|
| Hypothesis written | Done — parent doc |
| Facilitator script | Done — `opencode_live.py` |
| Multi-trial live run | Done — 2026-07-30 |
| Classify vs H1–H5 | Done — this document |
| Meta reply updated | Done — `meta-reply-to-melissa-response-ids.md` |
| REPORT.md updated for 2026-07-30 | Done — see also `CURRENT-EVIDENCE.md` |
| Support zip refreshed | Done — `meta-support-attachment/` + zip |

## 12. One-sentence conclusion

**Live OpenCode confirms H1:** muse-spark-1.1 systematically fails to preserve the user-supplied smoke filename under a real coding-agent harness, matching the severity of the strongest fixed-envelope (B2) API-replay signal and falsifying the idea that the bug is only a frozen-fixture curiosity.
