# Publication decision: blog post vs keep private

**Purpose:** Decide when to publish a public blog post about this defect (or update one later), without re-deriving process from chat history.  
**Scope:** Reliability / tool-use fidelity write-up about `muse-spark-1.1` identity-like path substitution under agentic context — not a security advisory process unless Meta or facts force that reframe.  
**Related:** [`CURRENT-EVIDENCE.md`](CURRENT-EVIDENCE.md) (rates), [`REPORT.md`](REPORT.md) (vendor narrative), [`meta-reply-to-melissa-response-ids.md`](meta-reply-to-melissa-response-ids.md) (2026-07-31 1.1 package, sent), [`meta-reply-to-melissa-1.2-clear.md`](meta-reply-to-melissa-1.2-clear.md) (1.2-clear follow-up, **sent 2026-08-08 18:03 EDT**), [`README.md`](README.md) (repo still private staging).

**Last reviewed:** 2026-08-19

---

## 1. Current recommendation (snapshot)

| Item | Status |
|---|---|
| Public blog post | **Published 2026-08-19** at https://stephens.page/blog/the-filename-i-asked-for/ |
| Existing Muse-specific blog post | **Live** - `the-filename-i-asked-for` on stephens.page/blog (portfolio commit `8863c30`) |
| Private Meta channel | **Delivered** — Melissa email sent **2026-07-31 ~11:46 local** with rates, OpenCode/factory-seat impact, envelope SHAs, and full B2/B12 `resp_…` tables. **Acknowledged 2026-08-03** (see §1.3) |
| Private repro repo | Still private; README: not approved for public release |
| Evidence maturity for a technical post | **High** for 1.1 failure *and* for 1.2 clearance (2026-08-05: B2 0/10, B12 0/10, live OpenCode 0/10) |

**Default path:** private handoff done → acknowledged + fair window elapsed → 1.2-clear courtesy follow-up → draft “was broken / now clear on 1.2” → scrub → publish.  
**Not waiting for:** root cause, immutable serving revision, or Meta’s permanent blessing.

### 1.1 Green-light checklist (as of 2026-08-19)

| ID | Condition | Status |
|---|---|---|
| **A** | Private report delivered | **Yes** — sent 2026-07-31 11:46 (rates + response IDs + impact) |
| **B** | Fair window | **Yes, two ways** — (1) explicit Meta acknowledgment **2026-08-03**: issue forwarded to the technical team, no hold requested (§1.3); (2) 8 calendar days elapsed, past the 7-day mark of 2026-08-07 |
| **C** | Stalemate after handoff | N/A — B satisfied |
| **D** | No contractual bar | **Re-verified 2026-08-19** against the live ToS (last-updated stamp still August 5, 2026). §10.1(xi) still purpose-based; §10.1(ix) carve-out intact; §10.1(x) still qualified by reconstruct/approximate. See **§1.2** |
| **E** | Facts still hold / dated history | **Yes** - 1.1 multi-day failure series; 1.2 multi-channel 0/30 wrong |
| **F** | Scrubbed artifacts ready | **Yes** - published page and agents.md contain zero `resp_…`, support-thread text, secrets, or `$HOME` paths |

**Published 2026-08-19.** Courtesy window targeted Monday 2026-08-17 (earliest defensible Friday 2026-08-14). No Meta reply to the 2026-08-08 offer-to-hold as of publish time (11 days). Live ToS re-read immediately before publish. Standing framing constraints kept: do **not** claim Meta closed the ticket, and do **not** claim 1.2 shipped *because of* the report.

Keep the standing framing constraints: do **not** claim Meta closed the ticket (it is open — "will be in touch when we have an update"), and do **not** claim 1.2 shipped *because of* the report.

### 1.2 Contractual / ToS check (Gate D)

#### 1.2.0 Re-verification after the 2026-08-06 terms update — checked 2026-08-08

Meta emailed **2026-08-06** ("We're updating the Meta Model API Terms of Service") announcing updates to the ToS, AUP, Model Designation and Geographic Use Policy, and Data Commitments, effective that day. The 2026-08-05 Gate D check below therefore had to be redone. Pages are client-side rendered — `WebFetch` returns only the shell; read them in a browser.

**Result: Gate D still passes. The two clauses the original analysis rested on survived the update verbatim, at unchanged numbering.**

| Clause | State after update |
|---|---|
| **§10.1(xi)** public benchmarks | **Unchanged, verbatim:** *"publicly disseminate performance benchmarks or evaluations of the Services for the purpose of promoting or marketing a competing product or service, without Meta's prior written authorization"*. Still **purpose-based** — the factory-seat evaluation framing remains outside it |
| **§10.1(ix)** competing models | Carve-out intact: *"using Services or Outputs solely for evaluation, benchmarking, or quality assessment of your own systems does not constitute a prohibited use"*. Now also reaches use "(including by taking Actions)" |
| **§12** Confidentiality | Substantively unchanged. Adds *"Your Content constitutes your Confidential Information"* — protects your side. Observed Outputs on your own prompts are still not clearly Meta Confidential Information; continue to omit `resp_…` anyway |

**Changed in a way that affects framing — §10.1(x) reverse engineering.** The clause now explicitly names **"harnesses"** and **"probing of inputs and outputs"** among prohibited methods. It remains qualified by purpose — the full phrase is *"or any other method designed to reconstruct or approximate the proprietary components of the Services"* — and fidelity testing is not designed to reconstruct proprietary components. **Blog implication:** describe the method as *black-box tool-argument fidelity testing on a fixed request envelope*. Do **not** describe it as "probing the model" or frame findings as inferences about internals, training data, or weights.

**AUP (updated same day) — reviewed 2026-08-08.** Nothing bars a reliability write-up. The vulnerability clause is unchanged ("Identify, scan for, or exploit vulnerabilities … without proper authorization"), so the fidelity-not-exploit framing in §2 still applies and no research exception is needed. New material is about *operating* agents, not publishing about them. Two notes for the repo rather than the post:

- New AUP language prohibits taking *"consequential or irreversible actions … including … executing destructive operations in production environments, without appropriate authorization, human oversight, review, and confirmation mechanisms."* `opencode_live.py --auto` and `muse exec --disable-approval` bypass approval **by design, in disposable workspaces** — that isolation is the safeguard. Keep it that way and keep saying so in the method description.
- New provenance clauses (don't strip watermarks/labels/metadata from Outputs) are not implicated by this work.

**Note:** the ToS page still displays *"Last updated: August 5, 2026"* even though the update email is dated 2026-08-06 and the new tier / Actions / provenance language is present. Treat the page content, not the stamp, as current.

#### 1.2.1 Original check — 2026-08-05

**Sources reviewed (public, self-serve Meta Model API preview terms):**

| Doc | URL |
|---|---|
| Meta Model API Terms of Service | https://ai.developer.meta.com/legal/terms-of-service (also https://dev.meta.ai/legal/terms-of-service) |
| Meta Model API Acceptable Use Policy | https://dev.meta.ai/legal/acceptable-use-policy |
| Geographic / model designation policy (linked from ToS) | https://ai.developer.meta.com/legal/geographic-use-policy |

ToS header notes (as extracted 2026-08-05): *“These Terms govern your access to and use of the Services for a **limited preview period**.”* Last updated **August 5, 2026**. Meta may update terms upon general public availability.

**Not reviewed / unknown:** any separate signed NDA, enterprise MSA, or private-partner addendum beyond the click-through Model API ToS. If you only used ordinary self-serve API access, the public ToS is the controlling public instrument.

| Topic | Finding | Blog implication |
|---|---|---|
| Blanket ban on discussing model behavior | **Not found** | Reliability narrative not per se forbidden |
| **§10.1(ix)** competing models / training | Ban on using Services/Outputs to train/improve competing models or systematically collect outputs for competing training data; **carve-out:** use solely for **evaluation, benchmarking, or quality assessment of your own systems** is not prohibited under that clause | Factory-seat / own-harness evaluation is aligned with the carve-out |
| **§10.1(xi)** public benchmarks | **Material clause:** you agree not to *“publicly disseminate performance benchmarks or evaluations of the Services **for the purpose of promoting or marketing a competing product or service**”* without Meta’s prior written authorization | Purpose-based. A factual “I evaluated Muse for my coding factory; 1.1 failed path fidelity; 1.2 cleared” post is **not** the same as marketing Claude/OpenAI/etc. Avoid “switch to X competitor” sales framing, affiliate-style competitor pitches, or leaderboard dunking that reads as promo for a rival |
| **§10.1(x)** reverse engineering / model extraction | Prohibits reverse engineering / systematic extraction of weights, algorithms, etc. | Stick to filename/tool-arg fidelity; don’t describe extraction or weight recovery |
| **§12 Confidentiality** | Protects non-public info disclosed by a party that is marked confidential or reasonably confidential (**including Account-related info**). API keys are confidential (elsewhere: do not share keys) | **Omit** API keys, auth material, private account internals. Observed model outputs on your own prompts are not clearly Meta Confidential Information, but **omit `resp_…` IDs** from the public post (vendor hygiene + avoid account-adjacent identifiers) |
| Feedback | Meta may freely use/disclose Feedback; Feedback is not your Confidential Information | Private Melissa report is fine; blog can paraphrase process, not paste support email |
| AUP | Bans unauthorized vulnerability exploitation, bypassing safety/rate controls, etc.; Meta may grant exceptions for legitimate cybersecurity research | Frame as **tool-use fidelity / reliability**, not a security exploit write-up; no need to claim AUP research exception |

**Gate D conclusion (operator judgment, not legal advice):** For a scrubbed **reliability / engineering-experience** post about 1.1 path substitution and 1.2 clearance under your own OpenCode/factory evaluation, the **public Meta Model API ToS does not appear to impose a hard ban**. The main risk clause is **§10.1(xi)** — keep the purpose **your evaluation and factory-seat decision**, not promoting a competing product. Re-read the live ToS before publish (terms can change). This is **not legal advice**.

Update this section when the recommendation changes.

### 1.3 Meta channel status (Gate B evidence) — as of 2026-08-08

| Date | Event |
|---|---|
| 2026-07-22 | Melissa opens: is this unexpected behavior, intended, or a security concern? |
| 2026-07-23 | Reply: unexpected; tool-use fidelity, not exploit; support zip attached |
| 2026-07-29 | Meta escalates to engineering as a **tool-use fidelity issue**; asks for response IDs |
| 2026-07-31 11:46 | 1.1 package sent: rates + full B2/B12 `resp_…` tables + factory-seat impact |
| **2026-08-03** | **Melissa: forwarded to the technical team, "will be in touch when we have an update to share," and "if you have anything new to add, feel free to reply back to this thread"** |
| **2026-08-08 18:03 EDT** (22:03 UTC) | **1.2-clear follow-up sent** ([`meta-reply-to-melissa-1.2-clear.md`](meta-reply-to-melissa-1.2-clear.md)): 0/30 multi-channel retest, new 1.2 envelope SHAs, 20 clean `resp_…` IDs, no root-cause claim — **plus notice of intent to publish and an offer to hold** |
| 2026-08-08 | No Meta reply yet to the follow-up. Ticket **open**, not closed |

**Gate B reading:** §3.1 B accepts *"Meta acknowledges investigation"* as an alternative to the calendar window; the 2026-08-03 message is that acknowledgment, and **no hold was requested** — so §3.2's "asked for short hold" red light is not triggered. The 7-day window also independently elapsed on 2026-08-07.

**Courtesy window created by the 08-08 send.** The follow-up explicitly offered to hold or adjust. That offer has to mean something: publishing before Melissa has a realistic chance to answer would make it hollow, which is worse for the record than not having offered at all.

Sizing it from **Meta's own demonstrated latency on this thread**, not from a guess:

| Sent | Replied | Turnaround |
|---|---|---|
| 2026-07-23 | 2026-07-29 | 6 days |
| 2026-07-31 | 2026-08-03 | 3 days |

The follow-up went out **18:03 EDT Saturday 2026-08-08**, so treat Monday **2026-08-10** as the first realistic read date. A typical reply then lands **2026-08-13 → 2026-08-16**.

- **Target: Monday 2026-08-17.** Clears their full observed range; weekday publishing; costs nothing since the post is dated history.
- **Earliest defensible: Friday 2026-08-14** — independently the +14d outer bound of the original fair window from the 07-31 package.

If she asks for a hold, calendar it with a specific revisit date. If she does not reply, publish — §3.1 C is explicit that a silent stall is not an indefinite veto, and Gates A/B/D/E were satisfied before this email went out.

**If she replies before publish**, revise the draft rather than appending: the *"ticket is still open"* line becomes false, and a confirmed fix would replace the deliberately agnostic "I can't tell you why" ending with a better one.

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
| Status | **published** |
| Path / URL | https://stephens.page/blog/the-filename-i-asked-for/ (agents.md companion at the same path) |
| First published | 2026-08-19 |
| Last updated | 2026-08-19 |

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
| Send Melissa reply with 2026-07-31 IDs + impact framing | **2026-07-31 ~11:46 local** (sent) | [x] |
| Meta acknowledges / engineering has package | **2026-08-03** — forwarded to technical team; no hold requested; ticket still open | [x] |
| Fair window end date (send + 7d / +14d) | **2026-08-07 — elapsed** / 2026-08-14 | [x] |
| Optional retest immediately before publish | **2026-08-05** 1.2 multi-channel 0/30 (done; optional 1.1 spot-check if still claiming live 1.1 breakage) | [x] |
| Gate D re-check after 2026-08-06 terms update | **2026-08-08** — §10.1(xi) unchanged, still purpose-based (§1.2.0) | [x] |
| Send 1.2-clear follow-up to Melissa | **2026-08-08 18:03 EDT** (sent) | [x] |
| Courtesy window after offer-to-hold (§1.3) | target **2026-08-17**; earliest **2026-08-14**; elapsed **2026-08-19** with no reply | [x] |
| Blog draft complete + scrubbed | **2026-08-08** - `blog-draft-tool-argument-fidelity.md` (scrub verified) | [x] |
| Re-read live ToS immediately before publish | **2026-08-19** - stamp still August 5, 2026; §10.1(ix)/(x)/(xi) unchanged from the 2026-08-08 check | [x] |
| Publish | **2026-08-19** https://stephens.page/blog/the-filename-i-asked-for/ | [x] |
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
