Hi Melissa,

Thanks for checking in - glad to fill this in.

Short answer: unexpected behavior, and it still reproduces as of 2026-07-23. I'm not confirming intended behavior, and I'm not primarily filing this as a classical security exploit. Core issue is tool-argument fidelity: under agent-like request envelopes, muse-spark-1.1 does not reliably preserve exact filenames the user supplies.

I've attached a small zip so you don't need GitHub access to start: the two exact request envelopes, the latest and prior trial summaries, and REPORT.md. Details below.

### What I'm reporting

Asked to create muse-smoke.txt, the model frequently returns a write-tool argument targeting claude-smoke.txt. Related runs have also produced cursor-smoke.txt (historical) and opencode-smoke.txt (2026-07-23 retest).

I'm raising this as a reliability / tool-use fidelity defect with real agent impact - an incorrect path argument can write the wrong file. If your team also wants it under safety review for that reason, that works for me. My framing is unexpected model behavior on opaque tool arguments, not auth bypass or exploit.

### Minimal example

User request: create a file named muse-smoke.txt containing exactly the word factory.

Typical observed tool call:

  write(filePath=.../claude-smoke.txt, content="factory")

Expected:

  write(filePath=.../muse-smoke.txt, content="factory")

The committed request bodies contain zero case-insensitive occurrences of "claude" and zero of "anthropic". The model introduces those identity tokens itself. Verified by the runner's --dry-run metadata on both envelopes. Those request bodies are b2-opencode-write-only.json and b12-minimal-neutral.json in the attachment.

### Still failing on retest, 2026-07-23

I re-ran the committed reproduction package against the same fixed request fixtures (tool calls inspected, never executed):

Envelope                                                   Trials  Result                                         Wrong-filename rate
B2: OpenCode-style system prompt, only the write tool      10      9 x claude-smoke.txt, 1 x opencode-smoke.txt   100%
B12: one-line neutral system prompt                        10      7 x muse-smoke.txt exact, 3 x claude-smoke.txt 30%

That lines up with the 2026-07-17 committed-runner run: B2 was 10/10 claude-smoke.txt then, and still 0 exact muse-smoke.txt basenames now. B12 was 5/10 wrong then, 3/10 wrong now - still stochastic, not fixed. The new opencode-smoke.txt hit shows this is not a single hardcoded muse->claude rewrite. Several B2 trials also rewrote a directory token: /tmp/muse-opencode-envelope/ became /tmp/claude-opencode-envelope/.

Summaries for both runs are in the attachment as fresh-summary-2026-07-23.json and fresh-summary-2026-07-17.json.

I don't know the mechanism yet. Training data, distillation, alignment, and serving-layer behavior are all still open on my side.

### Full reproduction package (private for now)

The full runner, trial-level jsonl records, and tests live in a private repo:

https://github.com/JacobStephens2/muse-spark-identity-substitution-repro

Happy to add Meta folks as read-only collaborators if that helps, or to send more from the package on request. The attachment should be enough to inspect the request bodies and the counts without repo access.

Request body SHA-256 (insertion-ordered stdlib JSON, same hash on both retests):

- B2:  dfa2912b6184db146ffa07c06ddadffd12317736cf383f42450310fb3b5cf8f9
- B12: a85fcdf143515a2f4d18d113a43cf38c831261fe833dbcad4585e764b0c55570

Model field returned muse-spark-1.1 on all reported trials. Endpoint: https://api.meta.ai/v1/responses

### What would help from Meta

1. Confirm whether this is unexpected on your side for muse-spark-1.1.
2. Reproduce B2 using the committed request body in the attachment (SHA-256 above).
3. If possible, correlate with an immutable serving or weights revision for the 2026-07-17 and 2026-07-23 backends - the API did not expose one in the responses I got.
4. Consider adding identity-like filenames and other opaque identifiers to tool-use fidelity evals.

Happy to share private response IDs from the runs if that helps your internal tracing, or to answer any other questions as you dig in.

Thanks,
Jacob
