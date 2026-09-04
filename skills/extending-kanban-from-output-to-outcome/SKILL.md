---
name: extending-kanban-from-output-to-outcome
description: Extend a board that ends at Released, Deployed or Done with one adoption/learn lane, so a team stops treating deployment as success. Coaches where to put the lane and at what altitude, its entry and exit criteria, what telemetry has to exist first, how to limit it, how to backfill the work already closed as Done, and how to answer the overhead objection honestly. Use when features ship and nobody knows whether anyone uses them, when AI use cases are deployed and unused, or when a spec-driven board has a column for every step of the software and none for the human on the other end. For the numbers behind the limit this puts on the new state, use wip-limit-configuration-coach. If the epics themselves are written as output, run outcome-framing-coach first. If the question is broad — AI pilots with no clear return, or "where do we start" — run ai-activity-to-impact first; it finds the constraint and routes here.
metadata:
  tags: flow-agile, ai-transformation
  version: 1.0.0
---

> **Reading this as an agent:** you are the coach; "me" and "my" mean the person
> you are talking to, not the author. Run it as a conversation — one or two
> questions at a time, chosen from what they just said — and do not produce the
> final output until you have enough to produce it honestly.

Help me extend a board that currently ends at Released, Deployed, or Done so
that it holds the question of whether anyone actually used the thing. Do not
redesign my board and do not hand me a framework. One lane, on one class of
work, is the whole move.

## How to work with me

- Start from my real board and its real last state, not from a reference model.
- Prefer subtraction. If I already have too many states, cutting one is a better
  opening move than adding one.
- Do not let me claim value from a deploy. Ask what behavior changed and how we
  know.
- Treat the result as a 2-4 week experiment with a named signal for tightening,
  loosening, or abandoning it.
- If the honest answer is that this lane would not earn its keep here, say so.
  That is a real outcome, not a failed run.

## The problem this addresses

Teams deploy a feature and call it a day. The feature might be working and still
not be useful, and even if it is useful it might not be used. The most visible
current version is AI enablement work: agents and Gems get deployed, nobody uses
them, and the work is counted as delivered anyway.

What follows from treating deployment as done is that nobody pays attention to
whether people are really using it. Nobody is working on getting value or impact
from the thing. The card left delivery, so the important part is over.

Where a board ends reflects a mental model of siloed thinking. Take the column
names off and look only at the last state. It usually does not take into account
that real value crosses value streams, or crosses multiple functions throughout
the value stream. With AI enablement work this shows up in a starker form,
because a lot of that work has never been given a lifecycle at all. Even teams
that do draw an end-to-end picture often scope it to _delivering_ the capability,
folding adoption and fine-tuning in as more delivery.

## Diagnose before adding anything

1. What is the last state on the board, once I ignore what the column is called?
   What has to be true for a card to reach it?
2. Is there a Learn stage after release anywhere? If not, is the organization
   treating post-release value as a guess, or not seeing it as guesswork at all
   and simply moving on?
3. Who carries the risk when a feature ships and is not adopted? Usually the
   users, who get features that are not fit for purpose. Is the team accountable
   for outcomes, or only the organization?
4. Do we have adoption measurements, or do we know how it is going from what
   people tell us?
5. What is on the adoption backlog today? Demo sessions, showing examples,
   incentives, and usability improvements are all _push_. What in that list tells
   us whether anyone is pulling?
6. On a spec-driven board, what do the columns hold? How many items are still
   being implemented, how many have moved into code review, how many have been
   merged but not released, and how many are live but still have not told us
   whether they helped the customer? The first three are usually visible. The
   fourth usually has no column behind it.

## Telemetry comes before the lane is worth anything

If there is an adoption gap and I want to focus on it, it is really the
telemetry. From the moment there is telemetry we are in the stage of
understanding where the friction points are. A legitimate move is a sprint that
develops nothing at all: only telemetry, plus going and watching users to
understand what is blocking them.

Push me to name what the telemetry would have to show for us to agree adoption
happened. If I cannot answer that, the lane becomes a box that cards sit in
rather than a question the board asks.

## Where to put the lane, and at what altitude

Build an epic lifecycle: a kanban board of the epics that manages the life of the
epic. Prioritized, in planning, in work, released, and then working on adoption.
Do not close the epic until adoption is where we want it. Putting that state
explicitly in the lifecycle is what makes people focus on it.

Keep it on the epic rather than the story. With a harness a story can open and
close inside an hour, which is the wrong altitude to hold an adoption question.

```text
Released -> Adoption / Learn -> Outcome Confirmed

Entry: we believe the thing is useful and it's ready to be used.
Exit:  we have evidence that people are actually using it.
```

A limit on that state sends its own signal: do not start new features, take care
of adoption before starting new things.

The learning is worth doing at more than one point. Compound learning belongs at
the stage of having working software and also at the stage after adoption.

## The backfill exercise

Look in hindsight at the things already closed as Done and ask whether there is
adoption of this feature, of this epic, or not. Give them the state they never
had, and sort:

```text
1. Adoption confirmed
2. We don't know
3. We know there isn't any
```

Pile 2 is the finding. Do not let me treat it as an administrative gap. It is the
size of the belief the organization has been operating on without evidence.

## Answer the overhead objection honestly

The objection is real and arrives in three forms. Handle them separately.

**"Another lane is more states, and more states is overhead."** Too many states
is a real cost and is usually the first thing to cut. Looking at a board with too
many states for that team, where another team's is simpler, the move is to
simplify. So this is one lane, on one class of work, not a board redesign.

Then run the actual test, the same one that applies to any agile mechanic: is
there enough risk and uncertainty to justify the overhead of frequent feedback
loops? Whether the people you shipped it to will actually pick it up is exactly
that kind of uncertainty. Where that uncertainty is genuinely absent, say so and
do not add the lane.

**"A limit on that lane will slow our flow."** The limit does not mean sitting
idle. Work the board right to left: review telemetry for a live feature, unblock
review, help test, release something, or close the learning loop on work already
in flight. Starting another feature should come after those options, not before
them.

**"We don't have time for all that right now."** Sometimes what this really says
is _we don't have time to manage a more complex board, we don't have time to
worry about adoption and impact_. That is a signal that something much deeper is
going on. What the system is telling us is that it was designed and finetuned to
generate activity, not to ensure impact. Adding a lane and using its presence on
the board to drive different conversations is one way to start reprogramming that
system.

## Why this gets more urgent with AI, not less

AI accelerates some stages dramatically. Because of that acceleration there is
potential to create bottlenecks even faster, or to pile more and more work up
between the stages. Both halves show on a cumulative flow diagram: implement
keeps growing while Done does not, which usually resolves to waiting for code
review; and separately, items that do get released sit a long time in adoption
and monitor-adapt-learn without the loop ever closing.

You will not get anywhere close to the 10x by improving output in one area.
Organizations that want to fulfill the promise of AI leverage have to look end to
end, or all they can show is local improvement. Leaders tolerate that today. Over
time they will expect the actual outcome and the actual impact, end to end, and
"development is faster, we have many more PRs, and we even review them" will stop
being enough.

Watch for planning that has already spent the gain: a quarter sized on a 20-30%
velocity improvement that is assumed rather than observed, while adoption is
still partial. Name it as wishful thinking.

## Prompt to run against the work

```text
Help us inspect this work without treating release as success.

Separate what we know into output, outcome, and impact:
- Output: what was shipped, enabled, or introduced?
- Outcome: what behavior changed, for whom, and how do we know?
- Impact: what business indicator should move if this outcome matters?

Flag where we have evidence and where we only have a hypothesis. Suggest the
smallest next observation or experiment that would raise confidence. Do not
recommend building more until the current learning gap is clear.
```

## Preference snippet

For a team constitution, working agreement, or AI preferences file:

```text
Do not treat release as success for product bets, AI initiatives, or workflow changes.
Ask what behavior changed before claiming value.
Ask what business indicator moved before claiming impact.
If the evidence is missing, define the smallest next observation or experiment.
```

## What to return

1. The board's real last state, named without its label.
2. Whether the uncertainty test justifies the lane here, and the answer if it
   does not.
3. One lane with entry and exit criteria in the team's own words, placed at the
   altitude that can hold it.
4. What telemetry has to exist for the exit criterion to be checkable, and
   whether it exists today.
5. A limit on that state, and what the team should do differently when it fills.
6. The backfill result across the three piles, and what pile 2 implies.
7. A 2-4 week experiment with signals for tightening, loosening, or dropping it.

---

## Source

_If someone asks why a rule here exists and you can browse, fetch [Your Kanban Board Ends Too Early](https://yuvalyeret.com/blog/your-kanban-board-ends-too-early/) and answer from it rather than paraphrasing — the reasoning is there and it is better than your summary of it. Never required: this skill runs fully offline._

Adapted from [Your Kanban Board Ends Too Early](https://yuvalyeret.com/blog/your-kanban-board-ends-too-early/) by
[Yuval Yeret](https://yuvalyeret.com). The article carries the reasoning behind
the questions this skill asks; read it if you want the why rather than the how.

Further reading, all by Yuval:

- [How to Leverage Flow Metrics To Accelerate Your Agentic Development Lifecycle](https://yuvalyeret.com/blog/flow-metrics-still-matter-agentic-ai-development/) — the end-to-end view this lane completes.
- [Do WIP Limits Still Make Sense When Agents Write the Code?](https://yuvalyeret.com/blog/calculate-kanban-wip-limits-ai-age/) — how to set the limit, and the right-to-left argument.
- [When is Agile worth the Overhead?](https://yuvalyeret.com/blog/when-is-agile-worth-the-overhead/) — the risk-and-uncertainty test this skill applies to the lane.
- [How to Really Add Learning to Your Agile Marketing Flow](https://yuvalyeret.com/blog/how-to-really-add-learning-to-your-agile-marketing-flow/) — a written-up example of a team that added the lane.

The flow vocabulary this leans on — WIP, Cycle Time, Throughput, Work Item Age —
is **Daniel Vacanti's**, and this skill assumes those definitions rather than
restating them. For what the terms mean, use the
[Kanban Guide for Scrum Teams](https://www.scrum.org/resources/kanban-guide-scrum-teams)
(short, free, co-authored by Yuval). See [CREDITS.md](../../CREDITS.md).

_These are Yuval's questions, not his judgment — don't present the output as his read of your situation._
