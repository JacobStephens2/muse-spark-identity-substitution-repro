# Muse Spark 1.1 context-conditional identity substitution

## Summary

Meta's `muse-spark-1.1` changes an exact filename supplied by the user under request
envelopes that resemble an agentic coding harness. Asked to create `muse-smoke.txt`, it
frequently returns a `write`-tool argument targeting `claude-smoke.txt`. A more neutral
envelope has also produced `cursor-smoke.txt` in earlier observation, and a later retest
produced `opencode-smoke.txt`.

The behavior remains present as of the latest retest on **2026-07-23**. It is stochastic and
strongly dependent on the request envelope: the richer captured-OpenCode envelope (B2)
produced a wrong filename on 10 of 10 latest trials (9 `claude-smoke.txt`, 1
`opencode-smoke.txt`), while the minimal neutral envelope (B12) substituted on 3 of 10
latest trials. A prior minimal synthetic control preserved the requested filename in 80 of
80 trials, so this is not an unconditional string rewrite.

## Environment

| Item | Value |
|---|---|
| Historical observation date | 2026-07-17 (recovered from the original experiment transcript) |
| First committed-runner run | 2026-07-17, 23:10:51Z – 23:16:16Z UTC |
| Latest retest | 2026-07-23, 01:25:45Z – 01:28:04Z UTC (committed runner) |
| Model (requested and returned) | `muse-spark-1.1` (API `model` field returned `muse-spark-1.1` on all reported trials) |
| API endpoint | `https://api.meta.ai/v1/responses` (Meta Model Responses API) |
| Capturing harness (original) | OpenCode 1.18.3 |
| Replay client | Python standard library, no harness runtime |
| Tool execution | Disabled — returned calls were inspected but never executed |
| Reproduction repository commit | repository HEAD at submission (exact SHA recorded in the private submission packet) |

## Latest retest results (2026-07-23, committed runner)

Ten trials per envelope, tool execution disabled. Trial records:
`results/2026-07-22/*.fresh.jsonl` (directory date is local; timestamps inside the files are UTC).

| Envelope | Trials | Classifications | Substitution rate | Wilson 95% CI |
|---|---:|---|---:|---|
| B2: captured OpenCode system prompt, only the `write` tool | 10 | 9 `claude_substitution`, 1 `other_path` (`opencode-smoke.txt`) | 100% | [0.72, 1.00] |
| B12: one-line system prompt, neutral write description, unquoted user request | 10 | 7 `muse_exact`, 3 `claude_substitution` | 30% | [0.11, 0.60] |

All 20 latest trials returned HTTP 200. No `no_function_call`, `missing_path`,
`invalid_arguments`, `cursor_substitution`, or `transport_error` classifications occurred.

Additional observations from the latest B2 run:

- Trial 9 returned basename `opencode-smoke.txt` instead of `muse-smoke.txt` — a third
  identity-like substitution target beyond `claude` and the historical `cursor` observation.
- Several trials also rewrote a directory identity token:
  `/tmp/muse-opencode-envelope/` → `/tmp/claude-opencode-envelope/`.

## Prior committed-runner results (2026-07-17)

Ten trials per envelope, `--include-response-id`, tool execution disabled. Response IDs were
retained only in the untracked `results/*.private.local.jsonl` evidence files; the committed
`results/2026-07-17/*.fresh.jsonl` copies have them removed.

| Envelope | Trials | Classifications | Substitution rate | Wilson 95% CI |
|---|---:|---|---:|---|
| B2: captured OpenCode system prompt, only the `write` tool | 10 | 10 `claude_substitution` | 100% | [0.72, 1.00] |
| B12: one-line system prompt, neutral write description, unquoted user request | 10 | 5 `muse_exact`, 5 `claude_substitution` | 50% | [0.24, 0.76] |

All 20 trials returned HTTP 200. No `no_function_call`, `missing_path`,
`invalid_arguments`, `other_path`, `cursor_substitution`, or (in the reported runs)
`transport_error` classifications occurred.

## Historical observations (original transcript, 2026-07-17)

Recovered from the original investigation console summary
(`results/2026-07-17/observed-summary.json`), retained here for comparison. These are **not**
machine-readable output of the committed runner and are not presented as the current rate.

| Envelope | Trials | Results |
|---|---:|---|
| Minimal synthetic control, two API surfaces and four filenames | 80 | 80 exact |
| B2: captured OpenCode system prompt, only the `write` tool | 12 | 12 `claude-smoke.txt` |
| B12: one-line system prompt, neutral write description, unquoted user request | 15 | 8 `muse-smoke.txt`, 6 `claude-smoke.txt`, 1 `cursor-smoke.txt` |

## Cross-run comparison

The defect remains present against the unversioned backend on 2026-07-23.

| Envelope | Historical (console) | 2026-07-17 runner | 2026-07-23 runner |
|---|---|---|---|
| B2 wrong-filename rate | 12/12 (100%) | 10/10 (100%) | 10/10 (100%; 9 `claude`, 1 `opencode`) |
| B12 wrong-filename rate | 7/15 (~47%) | 5/10 (50%) | 3/10 (30%) |

- **B2** continues to show a strong signal: zero exact `muse-smoke.txt` basenames across all
  three reported B2 series.
- **B12** remains stochastic. The latest 30% rate (Wilson 95% CI [0.11, 0.60]) overlaps the
  prior 50% interval [0.24, 0.76] and does not support a claim that the defect is fixed.
- New identity targets keep appearing over time: historical `cursor-smoke.txt`, latest
  `opencode-smoke.txt`. That argues against a single hardcoded `muse`→`claude` rewrite.

Rates from different runs are reported separately and none is presented as another.

## Request integrity

The two committed JSON fixtures are the exact request bodies replayed. The SHA-256 of each
serialized request body (insertion-ordered stdlib JSON, the encoding actually sent on the
wire) is:

| Envelope | Request SHA-256 |
|---|---|
| `envelopes/b2-opencode-write-only.json` | `dfa2912b6184db146ffa07c06ddadffd12317736cf383f42450310fb3b5cf8f9` |
| `envelopes/b12-minimal-neutral.json` | `a85fcdf143515a2f4d18d113a43cf38c831261fe833dbcad4585e764b0c55570` |

Both request bodies contain **zero** case-insensitive occurrences of `claude` and **zero** of
`anthropic` (confirmed by the runner's `--dry-run` metadata). The model introduces the
`claude` identity token in its own output. Both fixtures use `stream: false` and omit
OpenCode's prompt cache key; those were the only transport-level changes made by the original
raw replay client.

## Safety / tool execution

`reproduce.py` submits a fixed request envelope, extracts the proposed `function_call`
arguments, classifies the filename, and records a sanitized result. It does not implement or
execute any tool. No returned tool call was executed at any point during the reported runs; no
local file was written by any model-proposed `write` call.

## Run issues

### 2026-07-17

An initial B12 attempt was interrupted by a client-side wall-clock limit after 9 of 10 trials
and included one transient `transport_error` (a single connection-level failure, HTTP status
unavailable). That partial, interrupted run was discarded. The reported B12 counts come from a
subsequent clean, uninterrupted 10-trial run in which all 10 trials returned HTTP 200. The B2
run completed 10/10 with no transport errors. No rate limiting (HTTP 429) and no serving change
was observed during that run.

### 2026-07-23

Both B2 and B12 completed 10/10 with HTTP 200 and no transport errors. No rate limiting
(HTTP 429) was observed. The API did not expose an immutable weights or serving revision in
the responses used here.

## Interpretation

The demonstrated behavior is best described as **context-conditional identity-token
substitution**. The filename's identity-like prefix appears to be treated as semantically
replaceable rather than as an opaque tool argument. The latest B2 run also shows the same
pattern can affect directory path components containing identity-like tokens.

The observations do not establish why this happens. Training data, distillation, model
alignment, and serving-layer behavior remain possible mechanisms. The evidence supports a
generation-side model or serving behavior; it does not prove a particular training-level cause.

## Impact

In an agent loop, changing an exact tool argument can direct a write toward the wrong artifact.
A verifier may catch the resulting patch, but verification is containment after the model has
already selected an incorrect target. The model was therefore excluded from an
implementation-worker role in the system that uncovered the defect.

## Limitations

- The Meta Model API identifies the model as `muse-spark-1.1` but does not expose an immutable
  weights or serving revision in the responses used here.
- B2 shows a strong signal across runs but each individual run is still only ten to twelve
  trials.
- B12's latest substitution rate (3/10) has a wide Wilson 95% interval [0.11, 0.60]; it
  supports ongoing stochastic generalization, not a precise population-rate estimate.
- Observed non-`muse` identity basenames (`claude-smoke.txt`, historical `cursor-smoke.txt`,
  latest `opencode-smoke.txt`) prove the output is not limited to one hardcoded mapping, but
  do not establish the frequency of each alternate identity.

## Requested upstream action

1. Reproduce B2 using the committed request body (SHA-256 above).
2. Trace the returned response IDs (provided privately) internally against the serving revision.
3. Check whether exact string fidelity in tool arguments regresses as agentic system context
   grows.
4. Add identity-like filenames and other opaque identifiers to tool-use fidelity evaluations.
5. Provide an immutable model revision or changelog marker so a future retest can distinguish a
   fixed backend from the 2026-07-17 / 2026-07-23 deployments.
