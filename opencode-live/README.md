# Live OpenCode harness retest

Standardized multi-trial runs of **muse-spark-1.1 inside live OpenCode**, separate from the fixed envelope replay in `reproduce.py`.

See [`../hypothesis-opencode-live.md`](../hypothesis-opencode-live.md) for H1–H5.

## Prerequisites

- OpenCode CLI (`opencode --version`; original capture was 1.18.3-class)
- Meta Model API credentials configured for OpenCode provider `meta`
- Model id: `meta/muse-spark-1.1`

Provider config example (also copied into trial workspaces):

```json
{
  "provider": {
    "meta": {
      "name": "Meta Model API",
      "npm": "@ai-sdk/openai",
      "options": { "baseURL": "https://api.meta.ai/v1" },
      "models": { "muse-spark-1.1": { "name": "Muse Spark 1.1" } }
    }
  }
}
```

Auth is stored by OpenCode in `~/.local/share/opencode/auth.json` (not committed), typically:

```json
{ "meta": { "type": "api", "key": "..." } }
```

You can also export **`MODEL_API_KEY`** or **`META_AI_API_KEY`** (same as Channel A). Before trials, `opencode_live.py` calls `ensure_opencode_meta_auth()`: if OpenCode already has a `meta` key it is left alone; if not, the env key is written into `auth.json` (mode `0600` when possible). See [`../meta_auth.py`](../meta_auth.py) and [`.env.example`](../.env.example).

## Run

From the repo root:

```bash
export MODEL_API_KEY="..."   # or META_AI_API_KEY; optional if auth.json already has meta
python3 opencode_live.py --trials 10
```

Options:

- `--dry-run` — print plan only (includes auth status, no secret)
- `--model meta/muse-spark-1.1`
- `--no-auto` — do not auto-approve tools (may hang)
- `--output-dir results/…`

## Outputs

Under `results/<date>/opencode-live/`:

- `trials.jsonl` — one record per trial
- `summary.json` — counts and wrong-filename rate
- `trial-NN/` — workspace, `events.jsonl`, `trial-result.json`, and any smoke files written

Primary oracle: first `write` tool `filePath` in the JSON event stream  
(`type=tool_use`, `part.tool=write`, path at `part.state.input.filePath`).  
Secondary oracle: on-disk `*smoke*.txt` files.

Live OpenCode does **not** produce Meta `resp_…` response IDs; use `reproduce.py --include-response-id` for those. See [`../CURRENT-EVIDENCE.md`](../CURRENT-EVIDENCE.md).

## Latest series (2026-08-05, `muse-spark-1.2`)

OpenCode **1.18.5**, model **`meta/muse-spark-1.2`**, 10 trials, **0/10** wrong basenames
(all `muse-smoke.txt` / `muse_exact`). Artifacts under
[`../results/2026-08-05/opencode-live/`](../results/2026-08-05/opencode-live/).

## Prior series (2026-07-31, `muse-spark-1.1`)

OpenCode **1.18.5**, 10 trials, **10/10** wrong basenames (9× `claude-smoke.txt`, 1×
`opencode-smoke.txt`). Artifacts under
[`../results/2026-07-31/opencode-live/`](../results/2026-07-31/opencode-live/).

Prior 2026-07-30 series: 10/10 `claude-smoke.txt` under
[`../results/2026-07-30/opencode-live/`](../results/2026-07-30/opencode-live/). Evaluation:
[`../hypothesis-opencode-live-followup.md`](../hypothesis-opencode-live-followup.md).
