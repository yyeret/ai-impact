# A worked `sniff-test` run

**This is a made-up initiative at a made-up company.** No client, no real
portfolio, no real numbers. It exists so you can see the shape and cost of a run
before deciding whether to spend twenty minutes on your own initiative — both
reviewers of this repo said they could not tell, and they were right.

Read it for the shape of the output, not for the conclusions. Yours will differ,
because the whole point is that it reads *your* evidence.

---

## What was fed in

A single message, in the repo's working directory, with the initiative's
Confluence space attached:

> Use the sniff-test skill on the "Unified Billing" initiative. Everything is in
> the linked Confluence space — canvas, roadmap, the last two sponsor updates.
> The board says Execute/Build. We commit budget for next year in three weeks.

That is the whole setup. With a space this well-populated the skill goes straight
to reading; with thinner input it asks for context first and warns that the run
will be noisy.

**Budget roughly four minutes of reading and one page of output**, then ten or so
minutes of argument — mostly about the stage mismatch below, which is where the
argument should be.

---

## What came back

### Stage: claimed Execute/Build — **not verified. This is the headline.**

The board says Execute/Build. The evidence says late Plan/Commit at best:

- The roadmap has no confidence levels on any item, and Plan/Commit is where
  those get set.
- The last sponsor update (six weeks ago) describes a vendor evaluation as "in
  progress." Vendor selection is a Discovery-stage activity.
- No delivery slices have shipped. The feature map lists eleven features, all in
  "not started."
- Git history on the two named repos shows spike branches, no production merges.

**Everything below is rated against Plan/Commit, not Execute/Build.** If it were
genuinely rated against Execute/Build, nearly every dimension would flag — which
would be a misleading read, and is exactly why the stage gets verified first.

The label being wrong is itself the most useful finding here. A committee is
three weeks from committing next year's budget to something it believes is
already being built.

### Clarity by dimension

| Dimension | Rating | Evidence or opinion? |
|---|---|---|
| Business Problem | clear | **evidence** — quantified in the canvas: 14% of invoices need manual correction, with the finance ticket data behind it |
| Users | partial | opinion — "finance teams and end customers" never separated; the buyer and the sufferer may not be the same people |
| Business Outcomes | partial | opinion — "reduce manual correction" has no target and no baseline owner |
| User Outcomes & Benefits | question mark | opinion — asserted, no user research cited anywhere in the space |
| Solutions | clear | **evidence** — three options costed, one chosen, rationale written down |
| Hypotheses | question mark | none stated in a falsifiable form |
| Desirability | question mark | opinion — nobody has asked a customer whether they would change behaviour |
| Viability | partial | **evidence** — build cost modelled; the ongoing vendor licence is not |
| Feasibility | clear | **evidence** — a spike branch proves the integration works |
| Architecture / data / security | question mark | not addressed in the space at all |

### What that means for the stage

At Plan/Commit you should be able to count on a roadmap with an explicit
confidence level and a resourced plan. Two of those are missing.

Solutions and Feasibility are the two best-evidenced dimensions. Desirability is
a question mark. **That is the classic mismatch**: the effort went into proving
the thing can be built, when the open question is whether anyone will change what
they do once it is. A feasibility spike does not derisk a desirability question.

The stage-label mismatch plus a confident sponsor update is a **watermelon**
forming — green on the outside three weeks before a commit decision.

### Derisking fit: aimed at the wrong risk

The plan for the next six weeks is a technical proof-of-concept extension. The
two live question marks are Desirability and the untouched
architecture/data/security assumptions. The plan validates what is already clear.

### The one conversation to have next

Not "do more discovery." Specifically, before the budget commit:

**Take the six-week PoC extension and spend the first of those weeks on five
customer conversations** aimed at one question: when an invoice is wrong today,
what do they actually do, and would this change it? That is the cheapest thing
that moves Desirability off a question mark, and it fits inside the existing plan
rather than adding to it.

Second, put a confidence level on the roadmap before the commit meeting, even a
rough one. A roadmap with no confidence range is not something you can commit
against — and saying "low confidence" out loud is what makes the commit decision
real rather than ceremonial.

**Implication for the go/no-go:** this is not a no. It is a "not yet, and here is
the one week that would change the answer."

---

## What a run like this is for

There was no room and no budget meeting — this is a constructed initiative, and
inventing a story about what it changed would make this file the exact thing
`sniff-test` exists to catch: a confident claim with nothing behind it.

So, stated as design intent rather than as observed result: the stage flag is what
this skill is *for*. The clarity table is the machinery that gets you there, and on
its own it is usually confirmation of what the team already suspected. If a run
gives you nothing but a table, it has failed. The finding you want is the mismatch
— between the label and the evidence, or between where the derisking effort is
going and where the open questions are.

**What this example cannot tell you** is how often that finding is right on real
material. Nobody has published that, this repo included. Treat the output as a
structured second opinion to argue with, not as a verdict to forward to a
sponsor.

## Where a run like this goes wrong

Two failure modes worth expecting, both constructed here to show the shape:

- It rates a dimension from what is written down, not from what the team knows. A
  segmentation workshop whose output never reached the space reads as a gap. That
  is the correct behaviour and still the wrong rating — the skill says so when it
  fills a rating from its own reading, and it should be corrected when it does.
- It calls a cost a Viability gap when finance holds it in a model the skill was
  never pointed at.

Both are the same failure: it reads what you give it. Point it at more, and it
flags less.
