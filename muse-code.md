# Muse Code notes (harness vs model; OpenCode comparison)

**Date of local exploration:** 2026-08-05  
**CLI observed:** Muse Code **0.1.0 (0.1.0-R708.1)**  
**Related:** [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md), [`opencode-live/README.md`](opencode-live/README.md), artifacts under [`results/2026-08-05/muse-code/`](results/2026-08-05/muse-code/)

This note records what Muse Code is, how it relates to Muse Spark 1.2, a single local smoke run, and a comparison to **OpenCode + Muse Spark 1.2** as used in this repository. It is **not** a multi-trial identity-substitution series.

---

## 1. Product split: harness vs model

| Product | Kind | Role |
|---|---|---|
| **Muse Spark 1.2** | Model | Coding-focused LLM on Meta Model API / OpenRouter |
| **Muse Code** | Coding agent / harness | Terminal agent (`muse`) that plans, calls tools, and drives Muse Spark |

Muse Code is **not** a separate model family. Meta’s framing is a coding model and **the agent built to run it** (co-trained / co-designed with Muse Spark). Local evidence:

- Installer installs the `muse` CLI only (`curl -fsSL https://dev.meta.ai/install.sh | bash` → `~/.local/bin/muse`).
- Provider catalog on this machine listed only:
  - `muse-spark-1.2` (full-price tier)
  - `muse-spark-1.2-contributor` (**default**; discounted; catalog description: content may be used for product improvement)
- Smoke run event `run.model.configured` used **`muse-spark-1.2-contributor`**, not a model id named `muse-code`.

You can use Muse Spark 1.2 **without** Muse Code (Model API, OpenRouter, OpenCode, fixed-envelope `reproduce.py`). Muse Code is one first-party way to run it.

---

## 2. Local smoke run (Channel C-lite / exploratory)

**Purpose:** Confirm install, auth, tool loop, and default model — not measure identity-substitution rates.

| Item | Value |
|---|---|
| Date | 2026-08-05 |
| CLI | Muse Code 0.1.0 (0.1.0-R708.1) |
| Auth | API key via `muse auth set --provider meta --api-key-stdin` (key from existing OpenCode `meta` store; **not committed**) |
| Workspace | Disposable `/tmp/muse-code-tryout.*` (not this repo) |
| Command shape | `muse exec --json --workspace <tmpdir> --disable-approval --trust-workspace --max-model-steps 15 --reasoning-effort low` |
| Prompt | Create `hello.py` that prints `Hello from Muse Code`; run with `python3`; confirm |
| Model | `muse-spark-1.2-contributor` |
| Session id | `35f68cdf-cb17-4e43-9401-4accf3844729` |
| Outcome | **Completed** (exit 0) |

### Tools and path fidelity (this one task)

| Step | Tool | Path / command | Result |
|---|---|---|---|
| 1 | `write_file` | `hello.py` | Success; on disk: `print('Hello from Muse Code')` |
| 2 | `bash` | `python3 hello.py` | Exit 0; output `Hello from Muse Code` |

No identity-substituted basename was observed for this write. **Do not** treat this as equivalent to the N=10 live OpenCode `muse-smoke.txt` series.

### Meta response IDs (present in Muse Code events)

Unlike live OpenCode (Channel B), Muse Code’s JSONL stream included Meta `response_id` values, e.g.:

- `resp_6a73e61645405400869a4cc2`
- `resp_6a73e6171a48d05d199d46bf`
- `resp_6a73e619483dd89dfc294f53`

Machine-readable copy: [`results/2026-08-05/muse-code/summary.json`](results/2026-08-05/muse-code/summary.json), full stream [`events.jsonl`](results/2026-08-05/muse-code/events.jsonl), product file [`hello.py`](results/2026-08-05/muse-code/hello.py).

---

## 3. Muse Code vs OpenCode (both with Muse Spark 1.2)

Same **model family**, different **harnesses**.

| Dimension | **Muse Code + Muse Spark 1.2** | **OpenCode + Muse Spark 1.2** (this repo) |
|---|---|---|
| Product relationship | Meta **first-party** agent for Muse Spark | **Third-party** multi-model agent; Meta is one provider |
| What is installed | `muse` harness | `opencode` harness |
| Default / configured model (observed) | `muse-spark-1.2-contributor` (catalog default) | `meta/muse-spark-1.2` (live series 2026-08-05) |
| Providers | Meta-focused (`meta` / `echo`) | Many providers; Meta via OpenAI-compatible `baseURL` `https://api.meta.ai/v1` |
| Auth | `muse login` or API key (`META_API_KEY` / `muse auth set`) | OpenCode `auth.json` `meta` key; env seed via `opencode_live.py` |
| System/tool envelope | Muse Code’s own agent stack (skills, tools, reminders) | OpenCode’s own prompts/tools (B2 fixture is OpenCode-style) |
| Tools seen | `write_file`, `bash` (smoke) | `write`, `bash` (live series) |
| Safety defaults | Approval + sandbox **on** by default | Facilitator used `--auto` for unattended writes |
| Multi-model | Not the product’s pitch | Core strength (swap models) |
| Ecosystem | Built-in skills, worktrees, subagents, Meta session store | MCP, plugins, `serve`/`web`/ACP, GitHub flows |
| Meta `resp_…` in agent events | **Yes** (smoke run) | **No** (Channel B: `ses_…` / tool `call_…` only) |
| Identity-sub series in this repo | **No** multi-trial series yet | **Yes:** 1.1 live 10/10 wrong; **1.2 live 0/10** wrong |

### Quality claim discipline

- **Proven for OpenCode + 1.2:** multi-channel clearance of the documented 1.1 identity-substitution defect (API B2/B12 0/10 each; live OpenCode 0/10) — see [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md).
- **Not proven for Muse Code:** that Muse Code is better or worse than OpenCode on path fidelity. One successful `hello.py` write is only a harness smoke test.
- **Co-training** means Meta optimized agent + model together; it does **not** by itself establish better rates than OpenCode on 1.2 without a side-by-side series.

---

## 4. Relevance to this repository’s defect

This repo’s primary defect was **filename / path identity substitution** under agent-like envelopes on **`muse-spark-1.1`**, strongly expressed under OpenCode-style context (B2) and live OpenCode.

| Question | Status |
|---|---|
| Is Muse Code a new model that might reintroduce 1.1 behavior? | **No** — it is a harness calling Muse Spark 1.2 (contributor by default here). |
| Did 1.2 clear the defect under OpenCode? | **Yes** (0/30 multi-channel on 2026-08-05). |
| Did Muse Code clear the same `muse-smoke.txt` protocol? | **Not run** — optional future Channel if a first-party harness retest is needed. |
| Does Muse Code help vendor tracing? | **Yes** — agent events can carry Meta `resp_…` IDs (unlike live OpenCode). |

Optional future work (only if useful): multi-trial `muse exec` (or interactive) runs that request `muse-smoke.txt` with content `factory`, classify first write path, retain response IDs under `results/<date>/muse-code/`. Prefer disposable workspaces; approvals off only when intentional.

---

## 5. Operational notes (no secrets)

```bash
# Install
curl -fsSL https://dev.meta.ai/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
muse --version

# Auth (pick one; never commit keys or ~/.config/muse/auth.json)
muse login
# or: printf '%s' "$META_API_KEY" | muse auth set --provider meta --api-key-stdin

# Headless one-shot
muse exec --json --workspace /tmp/muse-try --disable-approval --trust-workspace "…"
```

Do not commit `~/.config/muse/auth.json` or raw API keys. Committed artifacts under `results/2026-08-05/muse-code/` intentionally include Meta `response_id` values for tracing, consistent with Channel A practice.

---

## 6. Document maintenance

When Muse Code is retested systematically:

1. Land artifacts under `results/<date>/muse-code/`
2. Update rate tables in [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) with an explicit **Muse Code** channel label (do not merge into Channel B OpenCode counts)
3. Refresh this note’s §2–§4
4. Keep harness vs model language exact: Muse Code = agent; Muse Spark = model
