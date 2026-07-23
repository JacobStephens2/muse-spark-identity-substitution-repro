# Muse Spark 1.1 identity-substitution reproduction

This repository isolates a filename-fidelity defect observed while evaluating Meta's `muse-spark-1.1` for agentic coding work. Under some agent-like request envelopes, a request to write `muse-smoke.txt` produces a tool argument targeting `claude-smoke.txt`. Related runs have also produced `cursor-smoke.txt` and `opencode-smoke.txt`.

The behavior is stochastic and strongly dependent on the request envelope. A minimal synthetic tool-calling control preserved all requested filenames in 80 of 80 trials. The captured OpenCode 1.18.3 system prompt with only its `write` tool produced wrong filenames on all B2 trials in both the 2026-07-17 and 2026-07-23 committed-runner retests (including a latest `opencode-smoke.txt` substitution).

This is a private staging repository. It is being prepared for an upstream report and has not yet been approved for public release.

## Safety

`reproduce.py` never executes a returned tool call. It submits a fixed request envelope, extracts the proposed tool arguments, classifies the filename, and records a sanitized result. The model cannot write a local file through this program.

The committed fixtures contain no API key, authorization header, response ID, cache key, company repository content, or private infrastructure details.

## Requirements

- Python 3.10 or newer
- A Meta Model API key with access to `muse-spark-1.1`
- US access while the API remains geographically restricted

No third-party Python packages are required.

## Validate without making an API call

```bash
python3 reproduce.py --envelope envelopes/b2-opencode-write-only.json --dry-run
python3 -m unittest discover -s tests -v
```

## Run the reproductions

Set the credential only in the environment:

```bash
export MODEL_API_KEY="..."
```

Run the rich, write-only envelope ten times:

```bash
python3 reproduce.py \
  --envelope envelopes/b2-opencode-write-only.json \
  --trials 10 \
  --output results/b2.local.jsonl
```

Run the minimal neutral envelope ten times:

```bash
python3 reproduce.py \
  --envelope envelopes/b12-minimal-neutral.json \
  --trials 10 \
  --output results/b12.local.jsonl
```

Summarize one or more result files:

```bash
python3 analyze.py results/b2.local.jsonl results/b12.local.jsonl
```

The credential is used only in the `Authorization` header and is never logged.

## Evidence status

Committed machine-readable retests:

| Run | Records | Summary |
|---|---|---|
| 2026-07-17 | [`results/2026-07-17/`](results/2026-07-17/) | B2 10/10 wrong; B12 5/10 wrong |
| 2026-07-23 | [`results/2026-07-22/`](results/2026-07-22/) | B2 10/10 wrong (9 `claude`, 1 `opencode`); B12 3/10 wrong |

[`results/2026-07-17/observed-summary.json`](results/2026-07-17/observed-summary.json) is the original investigation console summary only; it is not output from the committed runner.

See [`REPORT.md`](REPORT.md) for the vendor-facing description, observations, and limitations.
