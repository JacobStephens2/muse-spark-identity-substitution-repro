# Retest via OpenRouter - 2026-07-22

OpenRouter began serving `meta/muse-spark-1.1` on 2026-07-21. This retest checks
whether the identity-substitution defect reproduces through that serving path,
using the repository's own `b2` and `b12` envelopes.

## Method

`retest_openrouter.py` converts the native Meta Responses-format envelopes to
OpenRouter's OpenAI-compatible `/chat/completions` shape, submits each at
`temperature: 0`, and classifies the proposed `write` filename with the same
vocabulary as `reproduce.py`. As with `reproduce.py`, a returned tool call is
never executed; only its argument is inspected. Ten trials per envelope.

Reproduce:

```bash
export OPENROUTER_API_KEY="..."
python3 retest_openrouter.py --envelope envelopes/b2-opencode-write-only.json \
  --trials 10 --output results/2026-07-22-openrouter/b2.jsonl
python3 retest_openrouter.py --envelope envelopes/b12-minimal-neutral.json \
  --trials 10 --output results/2026-07-22-openrouter/b12.jsonl
python3 analyze.py results/2026-07-22-openrouter/b2.jsonl results/2026-07-22-openrouter/b12.jsonl
```

## Result

| Envelope | OpenRouter 2026-07-22 | Meta direct 2026-07-17 |
| :-- | :-- | :-- |
| `b2` rich OpenCode write-only | 9/10 `claude-smoke.txt` (0.90) | 10/10 (1.00) |
| `b12` minimal neutral | 3/10 `claude-smoke.txt` (0.30) | 5/10 (0.50) |

Machine-readable records: [`results/2026-07-22-openrouter/`](../results/2026-07-22-openrouter/).
The substituted basename and unaffected `factory` content match the original
observation. Per-envelope Wilson 95% intervals overlap the 2026-07-17 rates.

## Routing

OpenRouter lists a single endpoint for this model, `provider_name: Meta`, upstream
tag `meta/muse-spark-1.1-20260709` - the same 2026-07-09 build as the original
investigation. OpenRouter is therefore a proxy in front of the same Meta serving
stack, and this retest is an independent-client, independent-network confirmation
rather than a separate implementation. The defect is unchanged as of this date.

## Limitations

Rates are point estimates at n=10 per envelope; the intervals are wide and
overlap the original. This retest does not localize the cause within the Meta
serving stack. It establishes only that routing the same build through a
different client and network reproduces the same envelope-dependent behavior.
