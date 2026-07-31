# Muse Spark 1.1 identity-substitution reproduction

This repository isolates a filename-fidelity defect observed while evaluating Meta's `muse-spark-1.1` for agentic coding work. Under some agent-like request envelopes, a request to write `muse-smoke.txt` produces a tool argument targeting `claude-smoke.txt`. Related runs have also produced `cursor-smoke.txt` and `opencode-smoke.txt`.

The behavior is stochastic and strongly dependent on the request envelope. A minimal synthetic tool-calling control preserved all requested filenames in 80 of 80 trials. The captured OpenCode-style envelope (B2) has produced wrong filenames on all trials in every committed API-replay series. A **live OpenCode** retest (latest 2026-07-31, OpenCode 1.18.5) also produced **10/10** wrong basenames (mostly `claude-smoke.txt`).

This is a private staging repository. It is being prepared for an upstream report and has not yet been approved for public release.

**Start here for “what do we know today?”:** [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md)

## Safety

`reproduce.py` never executes a returned tool call. It submits a fixed request envelope, extracts the proposed tool arguments, classifies the filename, and records a sanitized result. The model cannot write a local file through this program.

`opencode_live.py` drives a **real OpenCode session**. With the default `--auto` flag, proposed tools **may execute** inside each trial workspace (and can rewrite absolute paths). Use disposable directories only.

The committed fixtures contain no API key, authorization header, cache key, company repository content, or private infrastructure details. Some retained result files intentionally include Meta `response_id` values for vendor tracing.

## Requirements

- Python 3.10 or newer
- A Meta Model API key with access to `muse-spark-1.1`
- US access while the API remains geographically restricted
- For live OpenCode runs: OpenCode CLI plus Meta provider auth (see [`opencode-live/README.md`](opencode-live/README.md))

No third-party Python packages are required for `reproduce.py`.

## Credentials (one export for both channels)

Set a key in the environment only (never commit it). Either name works:

```bash
export MODEL_API_KEY="..."          # preferred
# export META_AI_API_KEY="..."      # accepted alias
```

Optional local file (gitignored): copy [`.env.example`](.env.example) to `.env`, edit, then:

```bash
set -a && source .env && set +a
```

| Channel | How the key is used |
|---|---|
| **A** `reproduce.py` | Reads `MODEL_API_KEY`, else `META_AI_API_KEY`. Optional fallback: `--from-opencode-auth` or `MUSE_ALLOW_OPENCODE_AUTH=1` (reads OpenCode `auth.json` `meta.key` only when env is empty). |
| **B** `opencode_live.py` | Uses OpenCode’s auth store. If `meta` is missing there, seeds it from the same env vars (never overwrites an existing key). |

Shared resolution lives in [`meta_auth.py`](meta_auth.py). Keys are never printed; only the *source name* is logged to stderr.

## Validate without making an API call

```bash
python3 reproduce.py --envelope envelopes/b2-opencode-write-only.json --dry-run
python3 -m unittest discover -s tests -v
```

## Run the reproductions

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

## Live OpenCode harness

```bash
python3 opencode_live.py --trials 10 --model meta/muse-spark-1.1
```

See [`opencode-live/README.md`](opencode-live/README.md). Hypothesis and evaluation: [`hypothesis-opencode-live.md`](hypothesis-opencode-live.md), [`hypothesis-opencode-live-followup.md`](hypothesis-opencode-live-followup.md).

## Evidence status

Committed machine-readable retests:

| Run | Records | Summary |
|---|---|---|
| 2026-07-17 | [`results/2026-07-17/`](results/2026-07-17/) | B2 10/10 wrong; B12 5/10 wrong |
| 2026-07-23 | [`results/2026-07-22/`](results/2026-07-22/) | B2 10/10 wrong (9 `claude`, 1 `opencode`); B12 3/10 wrong |
| 2026-07-30 API replay | [`results/2026-07-30/b*.fresh.jsonl`](results/2026-07-30/) | B2 10/10 wrong; B12 4/10 wrong; response IDs retained |
| 2026-07-30 live OpenCode | [`results/2026-07-30/opencode-live/`](results/2026-07-30/opencode-live/) | 10/10 `claude-smoke.txt` |
| **2026-07-31 API replay** | [`results/2026-07-31/b*.fresh.jsonl`](results/2026-07-31/) | B2 **10/10** wrong; B12 **6/10** wrong; **response IDs retained** |
| **2026-07-31 live OpenCode** | [`results/2026-07-31/opencode-live/`](results/2026-07-31/opencode-live/) | **10/10** wrong (9 `claude`, 1 `opencode`) |

[`results/2026-07-17/observed-summary.json`](results/2026-07-17/observed-summary.json) is the original investigation console summary only; it is not output from the committed runner.

See [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) for the multi-channel map and [`REPORT.md`](REPORT.md) for the vendor-facing narrative.

## Document index

| Doc | Purpose |
|---|---|
| [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) | What is known today; channels; response ID locations |
| [`REPORT.md`](REPORT.md) | Vendor-facing write-up |
| [`meta_auth.py`](meta_auth.py) / [`.env.example`](.env.example) | Shared Meta API key resolution for both channels |
| [`opencode_live.py`](opencode_live.py) / [`opencode-live/`](opencode-live/) | Live OpenCode facilitator |
| [`hypothesis-opencode-live.md`](hypothesis-opencode-live.md) | Live-harness hypothesis |
| [`hypothesis-opencode-live-followup.md`](hypothesis-opencode-live-followup.md) | Hypothesis evaluation |
| [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md) | Current Melissa reply draft |
| [`meta-support-attachment/`](meta-support-attachment/) | Support zip source |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | OpenCode licensing notes |
