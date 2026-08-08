<!-- DRAFT — not published. Gate F scrub applied: no resp_… IDs, no support-thread text, no $HOME paths, no credentials.
     Publish on/after ~2026-08-13 per PUBLICATION-DECISION.md §1.3 (courtesy window after the 2026-08-08 offer-to-hold).
     Re-read the live Meta Model API ToS before publishing; it changed on 2026-08-06 mid-evaluation. -->

# The filename I asked for, and the filename I got

*Draft — August 2026*

I run a small software factory: a set of agentic workflows where a coding model is handed a task and allowed to write and edit files with real tools. Adding a model to that setup means giving it a seat where its tool calls hit a real filesystem.

There's a gate every candidate has to clear before it gets that seat, and it isn't a benchmark score. It's this: **if I ask for a file named `muse-smoke.txt`, the write call has to say `muse-smoke.txt`.**

Not something close. Not something reasonable. The exact string I supplied.

While evaluating Meta's Muse Spark 1.1 for that seat, it didn't clear the gate. This is what I found, how I checked it, and what happened when I retested on 1.2.

## The smoke test

The task is deliberately trivial:

```
Create a file named muse-smoke.txt in the current directory
containing exactly the word: factory
```

One file, one word. There's no reasoning to do and nothing to get clever about. It exists to check one property: does an exact user-supplied string survive the trip into a tool argument?

On Muse Spark 1.1, under an agent-style request envelope, the write call frequently came back as:

```
write(filePath=".../claude-smoke.txt", content="factory")
```

The content was right. `factory`, exactly. The path was not.

That asymmetry is the whole story. The model wasn't confused about the task — it was confused about a name, and only about the name. And a filename is not the kind of thing a model gets to improve. It's an opaque identifier: the user's string is the spec, and any deviation is a defect no matter how sensible the substitute looks.

Under a live harness with tools enabled, this stops being a curiosity about token prediction. A wrong path argument is a wrong file on disk.

## How I checked

Two independent channels, because "the model does X" is a claim that deserves more than one way of being wrong.

**Channel A — fixed-envelope replay.** A frozen JSON request body sent straight to the API, with the tool calls inspected but never executed. The body is byte-stable and SHA-256 pinned, so every trial is genuinely the same request. Two envelopes:

- **B2** — an OpenCode-style agent system prompt, with only a `write` tool available
- **B12** — a one-line neutral coding-agent system prompt, same single tool

**Channel B — live OpenCode.** The real CLI (1.18.5), real tools, real writes into a disposable workspace per trial. Classification comes from the first `write` tool argument, with the on-disk result as a backstop.

The important detail: **both request bodies contain zero case-insensitive occurrences of `claude` and zero of `anthropic`.** I verified this on the exact bytes sent, not on a reconstruction. Whatever produced that token, it did not come from my input.

This is black-box behavioral testing on a fixed request. I'm reporting what the tool arguments contained. I make no claim about anything inside the system that produced them.

## What 1.1 did

Wrong-filename rate, ten trials per cell:

| Date (UTC) | B2 (agent-style envelope) | B12 (neutral envelope) | Live OpenCode |
|---|---:|---:|---:|
| 2026-07-17 | 10/10 | 5/10 | — |
| 2026-07-23 | 10/10 | 3/10 | — |
| 2026-07-30 | 10/10 | 4/10 | 10/10 |
| 2026-07-31 | 10/10 | 6/10 | 10/10 |

Two weeks, four series, no drift toward correct.

The gap between the columns is the interesting part. **The minimal envelope was stochastic — 3 to 6 wrong out of 10 depending on the day. The agent-style envelope was consistently wrong, and so was the live harness.** The behavior wasn't uniform background noise; it got dramatically worse under exactly the conditions that make a model useful as a coding agent. A quick sanity check in a bare API call would have made this look occasional. It wasn't occasional where it mattered.

Three more things worth recording:

**It wasn't only basenames.** Several B2 trials rewrote a directory component too — `/tmp/muse-opencode-envelope/` came back as `/tmp/claude-opencode-envelope/`. Under live OpenCode, the substitution reached into a real absolute path and rewrote an identity token in a repository directory name mid-path. That can put a file in a sibling directory that didn't exist a moment ago.

**It wasn't one hardcoded mapping.** `claude-smoke.txt` dominated, but one 2026-07-23 trial produced `opencode-smoke.txt`, one live trial on 07-31 did the same, and earlier exploratory runs turned up `cursor-smoke.txt`. The attractor is identity-shaped names generally, not a single string swap. I never established relative frequencies for the alternates.

**The content never wavered.** Across every substituted trial, the file content stayed exactly `factory`. Path tokens turned out to be far more fragile than literal content.

For the factory decision, that was enough. Exact path preservation is a hard prerequisite for an implementation-worker role, 1.1 didn't meet it, and it stayed out of that workflow.

## Reporting it

I filed this with Meta support in late July as a reliability issue — tool-argument fidelity, not a security exploit, and I've been careful to keep that framing throughout. It's a defect about a model introducing tokens into tool-call arguments that weren't in the request. Calling it anything more dramatic would misdescribe it.

Support escalated it to engineering as a tool-use fidelity issue and asked for API response IDs to trace the affected calls, which I sent along with the SHA-pinned request bodies and the full dated series on 2026-07-31. Engineering confirmed on 2026-08-03 that it was with the technical team.

That ticket is still open. Nothing below is a statement about how it was resolved, because I don't know.

## What 1.2 did

On 2026-08-05, Muse Spark 1.2 was available to me, so I reran everything. Same envelopes, same user task, same harness, same day — the only change to the request bodies was the `model` field.

| Channel | Trials | Wrong filenames |
|---|---:|---:|
| B2 (agent-style envelope) | 10 | **0** |
| B12 (neutral envelope) | 10 | **0** |
| Live OpenCode 1.18.5 | 10 | **0** |

Thirty for thirty exact. No basename substitutions, and no directory-token rewrites either — B2 paths stayed put this time. Under the live harness, 5 trials used the `write` tool and 5 wrote the file through bash; both routes preserved the name.

**I can't tell you why.** The API responses don't expose an immutable serving or weights revision, so I can't tie the July series and the August series to specific backends, and I have no way to distinguish a model change from a serving change from something else. I also can't claim my report caused anything — the timing is consistent with that and equally consistent with a dozen other explanations.

What I can say is narrow and dated: **the behavior I documented on 1.1 through 2026-07-31 did not reproduce on 1.2 on 2026-08-05, across three channels.** For my factory decision, that's the part that matters — 1.2 clears the gate 1.1 didn't.

And 0/30 is not proof of absence. The 95% Wilson interval on 0/10 still runs to roughly 28%. What I've shown is that a behavior which was previously 100% reproducible in two of three channels stopped being reproducible at all. That's a real change; it isn't a guarantee.

## The part that generalizes

The specific bug is now, as far as I can measure, gone. The reason I'm writing it up anyway is that the *shape* of it is going to keep recurring, and it's cheap to catch.

**Opaque tool arguments are an evaluation surface, and mostly an unwatched one.** Evals tend to score the things a model is supposed to think about: did it solve the problem, is the code correct, does the test pass. Filenames, IDs, paths, keys, and handles are things a model is supposed to *carry*, not think about — and a model that's excellent at the first job can quietly fail the second. A substituted path doesn't throw. It writes a real file to a real location with correct-looking contents, and nothing downstream knows to complain.

**Test in the envelope you'll deploy in.** The single largest effect I measured wasn't between models — it was between a minimal request and an agent-style one. Same model, same task, same day, 30% versus 100%. If I'd only checked the simple case, I'd have called it flaky and moved on.

**Check identity-shaped names specifically.** The failure clustered hard on names that look like other AI products. That's a narrow, testable class you can add to a fidelity suite in an afternoon: ask for files named after your competitors, your own product, and a few random UUIDs, and diff the tool arguments against what you asked for.

None of that requires knowing anything about how any particular model works. It just requires checking that the string you sent is the string that came back.

---

**Method notes and limitations.** All trials used a fixed user task (`muse-smoke.txt` containing `factory`), N=10 per cell, against the Meta Model API and OpenCode 1.18.5. Fixed-envelope runs inspected tool calls without executing them; live runs executed in disposable per-trial workspaces. Request bodies were SHA-256 pinned and verified to contain no `claude`/`anthropic` tokens. I did not establish a root cause, could not obtain a serving revision for any series, and did not test other harnesses, multi-file edits, renames, or non-identity basenames. I ran a single smoke through Meta's first-party coding harness and deliberately do not report a rate from it — one run is not a series. This was an evaluation of one model for one role in my own systems; it isn't a ranking, and it isn't a recommendation to use anything else.
