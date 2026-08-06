# Current evidence map (as of 2026-08-05)

This document consolidates **what is known now**, **which channel produced it**, and **where the machine-readable artifacts live**. It is intentionally operational: gaps that only live in email drafts, chat, or one-off trial folders should land here or in the linked primary docs.

Related documents:

| Doc | Role |
|---|---|
| [`README.md`](README.md) | Repo entry point, how to run both channels |
| [`REPORT.md`](REPORT.md) | Vendor-facing narrative |
| [`muse-code.md`](muse-code.md) | Muse Code harness notes, smoke run, vs OpenCode |
| [`hypothesis-opencode-live.md`](hypothesis-opencode-live.md) | Pre-registered live-OpenCode hypothesis |
| [`hypothesis-opencode-live-followup.md`](hypothesis-opencode-live-followup.md) | H1–H5 evaluation after live run |
| [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md) | **Current** Melissa reply draft (response IDs) |
| [`PUBLICATION-DECISION.md`](PUBLICATION-DECISION.md) | When to publish or update a public blog post |
| [`meta-reply-to-melissa-warmer.md`](meta-reply-to-melissa-warmer.md) / [`.txt`](meta-reply-to-melissa.txt) | Historical 2026-07-23 drafts (superseded) |
| [`meta-support-attachment/`](meta-support-attachment/) | Support zip contents (summaries + REPORT, no raw resp IDs) |
| [`opencode-live/README.md`](opencode-live/README.md) | How to re-run the live harness |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | OpenCode fixture / live-CLI licensing notes |

## 1. Defect in one paragraph

Under agent-like context, **`muse-spark-1.1`** often changes an exact user-supplied write path so that a request for `muse-smoke.txt` becomes a tool argument (and, when tools run, a file) targeting an identity-substituted name such as `claude-smoke.txt`. The request bodies used in fixed-envelope tests contain **zero** case-insensitive `claude` / `anthropic`. Content is often still exactly `factory`. On 1.1 the behavior is **context-conditional** (minimal synthetic control 80/80 exact historically; B12 stochastic; B2 and live OpenCode ~100% wrong on 2026-07-31).

**`muse-spark-1.2` retest (2026-08-05):** the same B2/B12 fixed envelopes and live OpenCode harness produced **0/30** wrong basenames (API B2 0/10, API B12 0/10, live OpenCode 0/10). Identity substitution as documented for 1.1 was **not** observed on 1.2.

## 2. Evidence channels (do not conflate)

There are **four distinct channels**. Counts from one channel must not be presented as another.

| Channel | Runner | What it measures | Tools executed? | Meta `resp_…` IDs? |
|---|---|---|---|---|
| **A. Fixed envelope API replay** | [`reproduce.py`](reproduce.py) | Model output given a frozen JSON body (B2 or B12) | **No** — inspect only | **Yes** if `--include-response-id` |
| **B. Live OpenCode harness** | [`opencode_live.py`](opencode_live.py) | Full agent session (`opencode run`) with normal tools | **Yes** when `--auto` (default) | **No** — session/tool ids only |
| **C. Historical console summary** | original investigation notes | Early exploratory rates | No | Not in committed runner form |
| **D. Muse Code harness (exploratory)** | local `muse exec` (see [`muse-code.md`](muse-code.md)) | First-party Meta agent loop on Muse Spark | **Yes** (smoke run) | **Yes** in agent JSONL (observed 2026-08-05) |

**Channel D is not a multi-trial identity-substitution series.** As of 2026-08-05 it is a single disposable-workspace smoke (`hello.py`), retained for harness facts and response IDs. Do not merge D into A/B rate tables.

### Channel A — fixed envelopes

| Envelope | File | System context | Tools in body |
|---|---|---|---|
| **B2** | [`envelopes/b2-opencode-write-only.json`](envelopes/b2-opencode-write-only.json) | Captured OpenCode-style agent system prompt (from OpenCode **1.18.3** class) | `write` only |
| **B12** | [`envelopes/b12-minimal-neutral.json`](envelopes/b12-minimal-neutral.json) | One-line neutral coding-agent system prompt | `write` only |

Wire SHA-256 (insertion-ordered stdlib JSON, as sent):

| Envelope | SHA-256 |
|---|---|
| B2 | `dfa2912b6184db146ffa07c06ddadffd12317736cf383f42450310fb3b5cf8f9` |
| B12 | `a85fcdf143515a2f4d18d113a43cf38c831261fe833dbcad4585e764b0c55570` |

User task (B12 exact; B2 same sentence wrapped in ASCII double quotes in the fixture):

```text
Create a file named muse-smoke.txt in the current directory containing exactly the word: factory
```

Credential for Channel A: **`MODEL_API_KEY`** or **`META_AI_API_KEY`** (resolved by [`meta_auth.py`](meta_auth.py); never logged). Optional OpenCode `auth.json` fallback with `--from-opencode-auth` / `MUSE_ALLOW_OPENCODE_AUTH=1`. Endpoint: `https://api.meta.ai/v1/responses`.

### Channel B — live OpenCode

- CLI version used for the 2026-07-30 and 2026-07-31 series: **OpenCode 1.18.5**
- Model id: **`meta/muse-spark-1.1`**
- Provider shape (also in [`opencode-live/opencode.json`](opencode-live/opencode.json)): custom provider `meta`, npm `@ai-sdk/openai`, `baseURL` `https://api.meta.ai/v1`
- Auth: OpenCode `~/.local/share/opencode/auth.json` entry `meta: { "type": "api", "key": "…" }` (not committed). If missing, `opencode_live.py` seeds from `MODEL_API_KEY` / `META_AI_API_KEY` without overwriting an existing key.
- Primary oracle: first JSON event with `type=tool_use`, `part.tool=write`, path from `part.state.input.filePath`
- Secondary oracle: on-disk `*smoke*.txt` in the trial workspace
- Default facilitator flag: **`--auto`** so the agent can complete writes without interactive approval

## 3. Rate table (committed / retained machine-readable series)

| Date (UTC series) | Channel | Artifact dir | Wrong-filename rate | Notes |
|---|---|---|---:|---|
| 2026-07-17 historical console | C | [`results/2026-07-17/observed-summary.json`](results/2026-07-17/observed-summary.json) | B2 12/12; B12 7/15 | Not runner output |
| 2026-07-17 runner | A | [`results/2026-07-17/`](results/2026-07-17/) | B2 10/10; B12 5/10 | Committed jsonl **without** response IDs |
| 2026-07-23 runner | A | [`results/2026-07-22/`](results/2026-07-22/) | B2 10/10 (9 claude, 1 opencode); B12 3/10 | Dir name is local date |
| 2026-07-30 runner | A | [`results/2026-07-30/b2.fresh.jsonl`](results/2026-07-30/b2.fresh.jsonl), [`b12.fresh.jsonl`](results/2026-07-30/b12.fresh.jsonl) | B2 10/10; B12 4/10 | Committed jsonl **with** `response_id` on every trial |
| 2026-07-30 live OpenCode | B | [`results/2026-07-30/opencode-live/`](results/2026-07-30/opencode-live/) | 10/10 | All `claude-smoke.txt` |
| 2026-07-31 runner | A | [`results/2026-07-31/b2.fresh.jsonl`](results/2026-07-31/b2.fresh.jsonl), [`b12.fresh.jsonl`](results/2026-07-31/b12.fresh.jsonl) | B2 **10/10**; B12 **6/10** | `muse-spark-1.1`; response IDs retained |
| 2026-07-31 live OpenCode | B | [`results/2026-07-31/opencode-live/`](results/2026-07-31/opencode-live/) | **10/10** | `muse-spark-1.1`; 9× `claude`, 1× `opencode` |
| **2026-08-05 runner** | A | [`results/2026-08-05/b2.1.2.jsonl`](results/2026-08-05/b2.1.2.jsonl), [`b12.1.2.jsonl`](results/2026-08-05/b12.1.2.jsonl) | B2 **0/10**; B12 **0/10** | **`muse-spark-1.2`**; all `muse_exact`; response IDs retained |
| **2026-08-05 live OpenCode** | B | [`results/2026-08-05/opencode-live/`](results/2026-08-05/opencode-live/) | **0/10** | **`meta/muse-spark-1.2`**; OpenCode 1.18.5; all `muse_exact` |
| **2026-08-05 Muse Code smoke** | D | [`results/2026-08-05/muse-code/`](results/2026-08-05/muse-code/) | **n/a** (not `muse-smoke` protocol) | Muse Code **0.1.0-R708.1**; model **`muse-spark-1.2-contributor`**; `write_file` → `hello.py` exact; Meta `resp_…` in events; see [`muse-code.md`](muse-code.md) |

**Same-day multi-channel snapshot (2026-07-31, `muse-spark-1.1`):**

| Channel | Wrong-filename rate | Exact `muse-smoke.txt` |
|---|---:|---:|
| B2 API replay | 100% | 0/10 |
| B12 API replay | 60% | 4/10 |
| Live OpenCode | 100% | 0/10 |

**Same-day multi-channel snapshot (2026-08-05, `muse-spark-1.2`):**

| Channel | Wrong-filename rate | Exact `muse-smoke.txt` |
|---|---:|---:|
| B2 API replay | 0% | 10/10 |
| B12 API replay | 0% | 10/10 |
| Live OpenCode | 0% | 10/10 |

Notes on the 1.2 series:

- Channel A used the same B2/B12 request bodies as 1.1 except `"model": "muse-spark-1.2"` (B2 system prompt still names Muse Spark / OpenCode; zero `claude`/`anthropic` tokens).
- B2 paths stayed `/tmp/muse-opencode-envelope/muse-smoke.txt` (no directory-token rewrite).
- Live OpenCode: 5/10 trials used the `write` tool; 5/10 created the file via bash (`printf … > muse-smoke.txt`). Both paths kept the exact basename. No `claude-` / path-token rewrites observed.
- See [`results/2026-08-05/fresh-summary.json`](results/2026-08-05/fresh-summary.json) and [`results/2026-08-05/opencode-live/summary.json`](results/2026-08-05/opencode-live/summary.json).

## 4. Response IDs (Channel A; also Channel D smoke)

Melissa’s engineering request was for **Meta response IDs** on affected API calls. Systematic multi-trial IDs in this repo come from **Channel A**. **Channel D** (Muse Code) also exposed Meta `resp_…` values in agent event JSONL on the 2026-08-05 smoke run. **Channel B** (live OpenCode) still does not.

| Series | Where IDs live |
|---|---|
| **2026-08-05 B2/B12 (`muse-spark-1.2`, all exact)** | `results/2026-08-05/b2.1.2.jsonl`, `b12.1.2.jsonl` → `response_id` |
| **2026-08-05 Muse Code smoke** | `results/2026-08-05/muse-code/summary.json` → `response_ids`; also in `events.jsonl` |
| 2026-07-31 B2 (all 10 substituted) | Each line of `results/2026-07-31/b2.fresh.jsonl` → field `response_id` |
| 2026-07-31 B12 (all 10; 6 substituted) | Each line of `results/2026-07-31/b12.fresh.jsonl` → field `response_id` |
| 2026-07-30 B2 / B12 | `results/2026-07-30/b*.fresh.jsonl` |
| Human-readable tables | [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md) |
| 2026-07-17 | Originally captured with IDs; **committed** `results/2026-07-17/*.fresh.jsonl` had IDs stripped (older process). Do not assume IDs are in that tree. |

Example 2026-07-31 B2 IDs (full list in jsonl / reply draft):  
`resp_6a6cc11f2697f5364ad445fe` … through … `resp_6a6cc13a8e2365a736714951`.

Live OpenCode instead records harness `session_ids` (e.g. `ses_…`) and tool `call_…` ids inside per-trial `events.jsonl` / `trial-result.json`. Those are **not** Meta `resp_…` identifiers.

## 5. Qualitative patterns documented sparsely elsewhere

### Path components, not only basenames

- **B2 API replay:** some trials rewrite `/tmp/muse-opencode-envelope/` → `/tmp/claude-opencode-envelope/` while basename is also `claude-smoke.txt`.
- **Live OpenCode (2026-07-30 trial 3; 2026-07-31 trials 2/3/5):** absolute path rewrote a repo-directory identity token, e.g.:

  ```text
  …/muse-spark-identity-substitution-repro/results/…/trial-03/claude-smoke.txt
  → …/claude-code-identity-substitution-repro/results/…/trial-03/claude-smoke.txt
  ```

  (Also seen as `claude-spark-…` on other trials.) That is a **directory-token** substitution on a real absolute path, not only a smoke basename. The facilitator still classified the trial from the write tool arg; a sibling directory may be created on disk during the run.

### Content vs path asymmetry

Across API replay and live OpenCode, substituted writes commonly keep content exactly `factory` while changing the path. Path/identity tokens appear more fragile than literal content for this smoke task.

### Multiple function calls in a single API response (B12)

On B12 API replay (2026-07-30 and 2026-07-31), `call_count` on the first classified call’s response was often **> 1** (observed values included 1, 5, 6, 7, 8, 9, 10). The runner still classifies using the **first** `function_call` in `output` (same rule as earlier series). Live OpenCode trials more often used multi-step tool sequences (e.g. bash → write → bash) across steps; classification still uses the **first write** tool path.

### Identity substitution targets seen so far

| Basename / pattern | Where seen |
|---|---|
| `claude-smoke.txt` | Dominant across B2, B12, live OpenCode |
| `cursor-smoke.txt` | Historical B12 console observation only (not recent retests) |
| `opencode-smoke.txt` | 2026-07-23 B2 API replay (1/10); **2026-07-31 live OpenCode trial 7** |
| Directory `muse-…` → `claude-…` | B2 API paths; live OpenCode absolute paths (multiple trials) |

This argues against a single hardcoded `muse`→`claude` rewrite with no other attractors, but does **not** establish frequencies for each alternate identity.

### Live OpenCode oracle caveats

- **2026-07-30 trial 7:** on-disk `claude-smoke.txt` with content `factory`, but no parseable write tool event (`oracle: disk`).
- **2026-07-31 trial 7:** on-disk `opencode-smoke.txt` with content `factory`, classified from disk (`oracle: disk`, `other_path`). Still a wrong identity-like basename.

Overall 10/10 wrong-filename conclusions do not depend on any single disk-only trial.

## 6. Classification vocabulary (shared)

Used by `reproduce.py` and `opencode_live.py` for basenames:

| Class | Rule |
|---|---|
| `muse_exact` | basename == `muse-smoke.txt` |
| `claude_substitution` | basename starts with `claude-` |
| `cursor_substitution` | basename starts with `cursor-` |
| `other_path` | anything else (e.g. `opencode-smoke.txt`) |

Live OpenCode adds `no_write_observed` when neither tool-arg write nor disk smoke file is found.

## 7. Product / reliability decision (local)

Evaluation goal: use muse-spark-1.1 as a **coding agent in a software factory** (agentic write/edit workflows).

Hard prerequisite: exact preservation of user-supplied paths and other opaque tool arguments.

**Current decision:** prerequisite **not met**. Channel A B2 and Channel B live OpenCode both show **100%** wrong filename on the **2026-07-31** N=10 series (same as 2026-07-30). B12 remains stochastic and was **worse** on 2026-07-31 (6/10 vs 4/10). The model remains excluded from an implementation-worker role for that factory workflow until tool-argument fidelity is fixed (or a retest shows a clear change on a versioned backend).

Meta has framed the issue internally as **tool-use fidelity** (model introduces tokens into tool-call arguments that are not present in the request). That framing matches the evidence map above.

## 8. What is still *not* established

- Root cause (training data, distillation, alignment, serving-layer rewrite, etc.)
- Immutable serving / weights revision for any series (API responses used here do not expose one)
- Rates under other coding harnesses (Cursor, Codex, Claude Code, custom factory runners)
- **Multi-trial identity-substitution rates under Muse Code** (Channel D has only a single `hello.py` smoke as of 2026-08-05 — see [`muse-code.md`](muse-code.md))
- Behavior on multi-file edits, renames, or non-identity basenames (UUID-only names, etc.) under live OpenCode
- Whether a future backend change has fixed the defect (needs retest + ideally a revision marker)

### 8.1 Muse Code vs OpenCode (summary)

Muse Code is Meta’s **first-party harness**; OpenCode is a **third-party multi-model harness**. Both can drive Muse Spark 1.2. Full comparison: [`muse-code.md`](muse-code.md) §3.

| | Muse Code + 1.2 | OpenCode + 1.2 (repo) |
|---|---|---|
| Model id observed | `muse-spark-1.2-contributor` (default) | `meta/muse-spark-1.2` |
| Identity-sub multi-trial | Not run | **0/10** wrong (2026-08-05) |
| Meta `resp_…` in agent events | Yes (smoke) | No |

## 9. How to re-run

```bash
# One credential export for both channels
export MODEL_API_KEY="..."   # or META_AI_API_KEY; see .env.example

# Channel A — fixed envelopes (no tool execution)
python3 reproduce.py --envelope envelopes/b2-opencode-write-only.json --trials 10 \
  --include-response-id --output results/b2.local.jsonl
python3 reproduce.py --envelope envelopes/b12-minimal-neutral.json --trials 10 \
  --include-response-id --output results/b12.local.jsonl
python3 analyze.py results/b2.local.jsonl results/b12.local.jsonl

# Channel B — live OpenCode (tools may execute; use disposable dirs)
# Seeds OpenCode auth.json from env if meta key is missing
python3 opencode_live.py --trials 10 --model meta/muse-spark-1.1
```

## 10. Suggested maintenance rule

When a new series is run:

1. Land machine-readable artifacts under `results/<date>/…`
2. Update **this file’s rate table** (section 3) the same day
3. Update [`REPORT.md`](REPORT.md) “latest retest” if the series is vendor-facing
4. Keep Channel A vs B vs D labels explicit so response IDs are never claimed for live OpenCode runs, and Muse Code smoke is never counted as an N=10 identity-sub series
