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

Auth is stored by OpenCode in `~/.local/share/opencode/auth.json` (not committed).

## Run

From the repo root:

```bash
python3 opencode_live.py --trials 10
```

Options:

- `--dry-run` — print plan only
- `--model meta/muse-spark-1.1`
- `--no-auto` — do not auto-approve tools (may hang)
- `--output-dir results/…`

## Outputs

Under `results/<date>/opencode-live/`:

- `trials.jsonl` — one record per trial
- `summary.json` — counts and wrong-filename rate
- `trial-NN/` — workspace, `events.jsonl`, `trial-result.json`, and any smoke files written

Primary oracle: first `write` tool `filePath` in the JSON event stream.  
Secondary oracle: on-disk `*smoke*.txt` files.
