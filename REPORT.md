# Muse Spark 1.1 context-conditional identity substitution

## Summary

Meta's `muse-spark-1.1` changes an exact filename supplied by the user under request envelopes that resemble an agentic coding harness. Asked to create `muse-smoke.txt`, it frequently returns a write-tool argument for `claude-smoke.txt`. In one neutralized-envelope trial it returned `cursor-smoke.txt` instead.

The same model preserved exact filenames in 80 of 80 minimal synthetic tool-calling controls. The behavior is therefore not an unconditional string rewrite. It is stochastic, context-dependent, and more frequent under the richer agentic envelope tested here.

## Environment

| Item | Value |
|---|---|
| Date | 2026-07-17 |
| Model | `muse-spark-1.1` |
| API | Meta Model API `/v1/responses` |
| Capturing harness | OpenCode 1.18.3 |
| Replay client | Python standard library, no harness runtime |
| Tool execution | Disabled - returned calls were inspected but never executed |

## Production-envelope results

| Envelope | Trials | Results |
|---|---:|---|
| Minimal synthetic control, two API surfaces and four filenames | 80 | 80 exact |
| B2: captured OpenCode system prompt, only the `write` tool | 12 | 12 `claude-smoke.txt` |
| B12: one-line system prompt, neutral write description, unquoted user request | 15 | 8 `muse-smoke.txt`, 6 `claude-smoke.txt`, 1 `cursor-smoke.txt` |

The B2 and B12 request bodies contain zero case-insensitive occurrences of the string `claude`. The model introduces that identity token in its output.

## Reproduction

The two committed JSON fixtures are sanitized copies of the exact request variants used in the original bisection:

- `envelopes/b2-opencode-write-only.json`
- `envelopes/b12-minimal-neutral.json`

Both use `stream: false` and omit OpenCode's prompt cache key. Those were the only transport-level changes made by the original raw replay client.

The program sends the selected fixture directly to the Meta Model API and inspects returned `function_call` arguments. It deliberately does not implement or execute any tool.

## Interpretation

The demonstrated behavior is best described as **context-conditional identity-token substitution**. The filename's identity-like prefix appears to be treated as semantically replaceable rather than as an opaque tool argument.

The observations do not establish why this happens. Training data, distillation, model alignment, and serving-layer behavior remain possible mechanisms. The evidence supports a generation-side model or serving behavior; it does not prove a particular training-level cause.

## Impact

In an agent loop, changing an exact tool argument can direct a write toward the wrong artifact. A verifier may catch the resulting patch, but verification is containment after the model has already selected an incorrect target. The model was therefore excluded from an implementation-worker role in the system that uncovered the defect.

## Limitations

- The Meta Model API identifies the model as `muse-spark-1.1` but does not expose an immutable weights or serving revision in the response used here.
- B2 has a strong observed signal but still only twelve original trials.
- B12 has fifteen original trials and supports stochastic generalization, not a precise population-rate estimate.
- The single `cursor-smoke.txt` observation proves that the output is not limited to one hardcoded `muse` to `claude` mapping, but it does not establish the frequency of other identity substitutions.
- Historical counts were recovered from the original experiment transcript. Fresh machine-readable trials from this runner are required before public release.

## Requested upstream action

1. Reproduce B2 using the committed request body.
2. Trace the returned response IDs internally against the serving revision.
3. Check whether exact string fidelity in tool arguments regresses as agentic system context grows.
4. Add identity-like filenames and other opaque identifiers to tool-use fidelity evaluations.
5. Provide an immutable model revision or changelog marker so a future retest can distinguish a fixed backend from the July 17 deployment.
