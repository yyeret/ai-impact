---
name: frame-intent
description: Frame intent for an agentic workflow with a desired outcome, explicit assumptions, and leading indicators so specification is grounded in purpose. Use before discovery or specification, when an initiative is described as the thing being built, or when a product, AI use case, internal capability, or operating change lacks evidence for steering. Produce a usable intent brief while coaching the human on outcome thinking and discovery through the decisions at hand. For wording alone use outcome-framing-coach; for investment readiness use sniff-test.
metadata:
  tags: product-strategy, ai-transformation
  version: 2.0.0
---

# Frame Intent

## Outcome

Give the next agent or workflow a desired outcome, a set of assumptions, and
leading indicators that ground specification and support steering through
evidence. The primary deliverable is usable intent. A secondary benefit is helping
the human understand why outcome framing, discovery, and evidence matter as they
work with agents. Do both through the same work.

## Outcome Indicators

- The next agent can specify or design a learning step without inventing the
  initiative's purpose, critical assumptions, or evidence for its next decision.
- An owner can use an early indicator to decide whether to continue, adjust,
  investigate, or stop before waiting for the final business result.
- When coaching is needed, the human can explain the relevant outcome, assumption,
  or indicator choice in their own context. An explanation delivered is not
  evidence that human behavior changed.

## Discovery Question

What intent and evidence should guide the agents before we specify what to build?

## Gotchas

- The initiative is never its own goal. "Roll out the copilot" names a solution;
  find the result someone would still own if that solution were cancelled.
- A polished brief does not make a belief true. Preserve unknowns rather than
  inventing baselines, targets, owners, or supporting evidence.
- An outcome is a change in what someone does. Tool usage and things shipped
  can miss the actual change in work; connect that change to a business result.
- A metric is leading relative to an outcome and a decision. State the causal
  belief and the action that different evidence could prompt.
- Coaching must not become a prerequisite course. Draft what context supports;
  ask only about gaps that change the next decision.

## Intake and working style

Read the supplied request, existing artifacts, and constraints first. Establish
the unit of work and the receiving workflow's native intake or spec format.
This skill works in conversation or from supplied material without requiring
a particular framework, tool, or web access.

With enough context, synthesize the brief directly and invite correction where
it matters. With thin context, ask one or two consequential questions at a time
and update the brief as answers arrive. Separate confirmed inputs, inferences,
proposals, and unknowns. If no human is available, produce a provisional brief
and flag decisions that still need an owner; never invent approval or block
useful drafting on an interview.

Coach when a choice needs explanation: briefly explain why a proposed goal is an
output, why an assumption needs discovery, or how an indicator changes a decision.
Use the person's example and invite correction. Adapt to familiarity and requests
for brevity; do not repeat understood lessons or add a mandatory quiz. The
artifact still has to be usable.

## Frame the intent

1. **Find the owned result.** State the desired outcome, accountable owner, why
   it matters now, and baseline, target, and time horizon where known. For
   "maintain" or "protect," establish today's result. Separate the buyer, the
   people doing the work, and the person whose numbers move.
2. **Identify the constraint and boundaries.** Name what plausibly holds the
   result back, evidence for that belief, non-goals, and hard constraints. Would
   fixing it require the proposed solution at all? Keep solutions as options.
   For mandatory compliance or safety work, state the fixed obligation honestly
   and investigate uncertainty about effectiveness or adoption where it exists.
3. **Name the change in work.** Which people or agents will do what differently
   compared with today, and how should that affect the result? For internal or
   technical work, include the downstream beneficiary. "People use the tool"
   is not enough; consider adoption alongside delivery.
4. **Expose assumptions.** State a falsifiable causal belief: if this change in
   work happens, this result should follow, because of this mechanism. Record
   critical assumptions, evidence for and against, confidence with a reason,
   and observations that would disprove them. Use stable IDs for handoff.
   Prioritize assumptions whose failure changes the bet; use desirability,
   usability, feasibility, and viability as prompts where useful.
5. **Choose leading indicators for steering.** Select a small set of early signals
   that could change the next decision. For each, give the linked outcome or
   assumption, why it should lead it, measure and population, baseline, proposed
   target or threshold, source, owner, review timing, and action different results
   would prompt. Mark missing values; collecting a baseline can be the next step.
   Distinguish early behavioral signals from final results and technical
   acceptance tests. Demos or completed work do not establish impact.
6. **Choose the next learning or delivery step.** With weak evidence for a critical
   assumption, recommend the smallest useful experiment: what to learn, how,
   by when, what changes the decision, and who decides. With sufficient evidence,
   hand intent to specification with remaining assumptions visible. Do not impose
   discovery when proportionate evidence already supports delivery. Record the
   owner and trigger for revisiting intent after release and adoption; shipping
   alone cannot establish that the outcome occurred.

## Output and handoff

Produce a concise intent brief with these contents, adapting headings to the
receiving framework rather than imposing a template:

- **Desired outcome:** owner, who does what differently, expected business result,
  baseline, target, and time horizon; label missing or proposed values.
- **Context and boundaries:** why now, constraint and evidence, scope, non-goals,
  fixed obligations, and solution options kept separate.
- **Assumptions and evidence:** causal hypothesis, critical assumptions, supporting
  and opposing evidence, confidence, and falsification signals.
- **Leading indicators and steering:** measures and causal links, baselines,
  targets or thresholds, sources, owners, review cadence, and implications for
  continuing, adjusting, investigating, or stopping.
- **Next decision:** discovery or specification, next learning step where needed,
  decision owner, timing, unresolved questions, and outcome-review trigger.
- **Status of claims:** confirmed, inferred, proposed, and unknown separated.

Use the caller's existing artifact or native spec section as the canonical home.
If a standalone file is needed, use an intent-named Markdown file in the actual
workspace, such as `intent.md`, and link it from the receiving spec. In chat-only
settings, return the brief in chat. Do not create a competing copy or change a
receiving framework's schema or instructions without authorization.

Tell the receiving agent to preserve the outcome, assumption IDs, and indicator
links when deriving scenarios, requirements, or an experiment. Architecture and
stack choices belong to planning unless supplied as hard constraints. Flag gaps
that prevent a particular decision without discarding the usable brief.
Human approvals remain human.

## Boundaries

- Wording of a well-framed epic → `outcome-framing-coach`.
- Investment readiness → `sniff-test`.
- Patterns across initiatives → `sniff-test-portfolio`.
- Broad AI activity without a defensible result → `ai-activity-to-impact`.
- Detailed requirements and implementation design → the receiving workflow's
  specification and planning steps. This skill supplies their intent.

For maintenance or evaluation, read [references/tests.md](references/tests.md)
for trigger cases and behavioral acceptance scenarios.

## Source

Evolved from this repository's `business-initiative-coach`. The intent handoff and
coaching through workflow decisions reflect [Yuval Yeret's](https://yuvalyeret.com)
practice. Broader exploration is tracked in
[portfolio-pdlc issue 11](https://github.com/yyeret/portfolio-pdlc/issues/11).

Inspired by the **Lean Product Canvas**, by **Jeff Gothelf and Josh Seiden**:
business results, users, falsifiable hypotheses, and the smallest useful learning
step. "Who does what by how much" is their phrasing. This skill uses its own
intent brief and does not reproduce their canvas. Get the original material from
[Sense & Respond](https://www.senseandrespond.co/the-lean-product-canvas) or
[Jeff Gothelf](https://jeffgothelf.com/blog/the-lean-product-canvas/).
Sense & Respond Learning offers Lean Product Discovery through Certified Training
Partners, including Yuval; that recommendation carries an interest.
See [CREDITS.md](../../CREDITS.md) for the wider lineage.

These are Yuval's methods, not his personal assessment of a particular initiative.
