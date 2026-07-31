# Publication decision: blog post vs keep private

**Purpose:** Decide when to publish a public blog post about this defect (or update one later), without re-deriving process from chat history.  
**Scope:** Reliability / tool-use fidelity write-up about `muse-spark-1.1` identity-like path substitution under agentic context — not a security advisory process unless Meta or facts force that reframe.  
**Related:** [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) (rates), [`REPORT.md`](REPORT.md) (vendor narrative), [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md) (private email draft), [`README.md`](README.md) (repo still private staging).

**Last reviewed:** 2026-07-31

---

## 1. Current recommendation (snapshot)

| Item | Status |
|---|---|
| Public blog post | **Do not publish yet** |
| Existing Muse-specific blog post | **None found** (personal blog / portfolio have other agent posts; no Muse Spark identity-substitution article) |
| Private Meta channel | Open — response IDs + 2026-07-31 retest in reply draft; confirm whether latest draft was **sent** |
| Private repro repo | Still private; README: not approved for public release |
| Evidence maturity for a technical post | **High** (multi-day B2 100%, live OpenCode 100%, B12 stochastic) |

**Default path:** finish private handoff → fair vendor window → then draft/publish.  
**Not waiting for:** root cause, immutable serving revision, or Meta’s permanent blessing.

Update this section when the recommendation changes.

---

## 2. What kind of publication this is

Treat this as a **reliability research / engineering experience** post unless new facts show intentional unsafe behavior or a classical vulnerability class.

| Framing | Use |
|---|---|
| **Preferred:** tool-argument fidelity; coding agent reliability; factory-seat gate | Blog, talks, public repro later |
| **Avoid as lead:** “exploit,” “bypass,” dunking on Meta, security theater | Inflates risk and confuses Meta’s tool-use-fidelity track |
| **Optional secondary note:** wrong path → wrong write on disk under live harness | True impact; keep proportional |

If Meta or you later reclassify as security, pause public posting and follow a disclosure path appropriate to that class (this doc does not define a full VDP process).

---

## 3. Decision: first publish (new post)

### 3.1 Green lights (publish when several are true)

Prefer **at least A + B**, or **C alone** after a real handoff:

| ID | Condition | Notes |
|---|---|---|
| **A** | Private report delivered | Melissa/support has the issue, current rates, and response IDs (or an explicit path to them). Draft alone is not enough. |
| **B** | Fair window elapsed | Roughly **1–2 weeks** after engineering has actionable IDs/package, **or** Meta acknowledges investigation / fix / “no further info needed.” |
| **C** | Stalemate after handoff | No substantive reply after a clear package + reasonable follow-up; silent stall is not an indefinite veto. |
| **D** | No contractual bar | No NDA, private-preview, or access terms that forbid public discussion of model behavior. |
| **E** | Facts still hold | Retest (or recent series) still shows material wrong-filename rates on B2 and/or live OpenCode — or you publish a “was broken / now fixed” story with dates. |
| **F** | Scrubbed artifacts ready | Post and any public repo omit secrets, response IDs, personal absolute paths, private email quotes beyond fair paraphrase. |

### 3.2 Red lights (do not publish yet)

| Condition | Why |
|---|---|
| Latest IDs/rates not yet sent | Public post races unfinished private channel |
| Meta actively investigating and asked for short hold | Honor brief professional holds; calendar them |
| Only weak / single-channel evidence | Not the case as of 2026-07-31; if a future retest flips, revisit |
| Post would include API keys, auth.json, private email full text, or response IDs | Operational and vendor-tracing hygiene |
| Intent is to pressure Meta mid-escalation | Prefer accuracy + process over leverage |

### 3.3 What you are *not* waiting for

- Perfect causal story (training vs serving vs alignment)
- Immutable model revision ID (nice if Meta provides one; not a publish gate)
- 100% B12 rate (stochastic neutral envelope is already documented)
- Public approval from Meta forever

### 3.4 Suggested first-post shape

Keep the post self-contained; link a public repro only if/when the repo is opened.

1. **Hook:** evaluating Muse for a software-factory coding seat; exact path fidelity is a hard gate.  
2. **Behavior:** user asks for `muse-smoke.txt` → tool arg / file often `claude-smoke.txt` (sometimes other identity-like names).  
3. **Controls:** minimal envelope often exact; OpenCode-style and live OpenCode ~always wrong on recent N=10 series.  
4. **Impact:** cannot reliably put Muse in OpenCode for agentic write/edit work.  
5. **Reporting:** reported privately as tool-use fidelity; multi-day retests still reproduce as of DATE.  
6. **Ask of readers / vendors:** treat opaque tool args as fidelity eval surface.  
7. **Limitations:** stochastic B12; no public serving revision; not a claim about all Meta models.

---

## 4. Decision: update an existing post

As of the last review, **no Muse-specific blog post exists**. When one does (or if you discover a draft elsewhere), use this section.

### 4.1 When to update

| Trigger | Action |
|---|---|
| Material rate change (e.g. B2 or live OpenCode no longer ~100% wrong) | Update headline rates + date; say what changed |
| Meta ships a fix or named revision | Add “status after DATE” section; retest before claiming fixed |
| New channel (e.g. another harness) changes the story | Add channel table; don’t overwrite prior dates |
| Correction (wrong rate, wrong OpenCode version, overclaim) | Correct in place; note correction date briefly |
| Repo goes public or URL changes | Add/update link |
| Framing was too harsh or too soft vs evidence | Tone pass only if facts still match |

### 4.2 When *not* to thrash the post

- Day-to-day B12 wobble within wide Wilson intervals (e.g. 4/10 → 6/10) — optional footnote, not a new essay  
- Pure process updates (email sent, zip rebuilt) — keep in this repo, not the blog  
- Adding every response ID or trial path — private / vendor-only  

### 4.3 Update checklist

- [ ] Retest or cite latest committed series (`results/YYYY-MM-DD/`, [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md))  
- [ ] Keep historical rates with dates; don’t erase prior evidence  
- [ ] Re-scrub paths, IDs, credentials  
- [ ] Align title/lede with current factory-seat decision  
- [ ] If claiming fixed: both Channel A (B2) and Channel B (live OpenCode) should clear the bar, or state clearly which channel improved  

### 4.4 Possible post locations (operator notes)

These are **not** Muse posts today; listed so future updates know where agent writing usually lands:

- Personal blog repo: `jacob-stephens-blog`  
- Portfolio-style posts: `portfolio/blog/` (other agent/infra pieces)  

When a Muse post is created, record its path/URL here:

| Field | Value |
|---|---|
| Status | **not created** |
| Path / URL | — |
| First published | — |
| Last updated | — |

---

## 5. Private vs public artifact matrix

| Artifact | Private (now) | Public later (if opened) |
|---|---|---|
| Rates, envelope hashes, method | OK in blog (summary) | Full runners + fixtures |
| Meta `resp_…` response IDs | Vendor email / private results only | **Omit** from blog |
| Melissa draft full text | Private | **Omit**; paraphrase process only |
| Live OpenCode absolute paths under `$HOME` | Redact in public prose | Prefer relative trial paths |
| Support zip | Attach to Meta only | Optional public summary JSON without IDs |
| API keys / auth.json | Never | Never |

---

## 6. Timeline template (fill in as you go)

| Milestone | Target / actual | Done? |
|---|---|---|
| Send Melissa reply with 2026-07-31 IDs + impact framing | — | [ ] |
| Meta acknowledges / engineering has package | — | [ ] |
| Fair window end date (e.g. send date + 14 days) | — | [ ] |
| Optional retest immediately before publish | — | [ ] |
| Blog draft complete + scrubbed | — | [ ] |
| Publish | — | [ ] |
| If repro goes public: link from post | — | [ ] |

---

## 7. One-page go/no-go

**Publish a new post only if:**

1. Private handoff is real (not just a local draft), **and**  
2. Fair window or explicit Meta close/stall, **and**  
3. No contractual bar, **and**  
4. Latest evidence still supports the claims (or the post is a dated history), **and**  
5. Scrub checklist passes.

**Update an existing post only if:**

1. A material technical or status change exists (fix, correction, new channel, factory-seat flip), **and**  
2. You keep dated history, **and**  
3. Scrub checklist still passes.

**Otherwise:** keep private; retest when Meta claims a fix or when you need fresh factory-seat data.

---

## 8. Maintenance

When something material changes (email sent, Meta reply, fix observed, post published):

1. Update **§1 Current recommendation** and **§6 Timeline**.  
2. If a post exists, fill **§4.4**.  
3. Optionally note the decision in [`HANDOFF.md`](HANDOFF.md) one-liner.  
4. Do not treat this file as vendor-facing; Meta packet stays [`REPORT.md`](REPORT.md) + support zip.
