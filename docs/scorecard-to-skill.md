# Turning a scorecard into a reflection skill

The scorecards at [yeretagility.com](https://yeretagility.com) and the skills in this
repo look like the same thing and are not. This note says what actually carries over,
what should be thrown away, and what has to be added — so the next conversion does not
have to re-derive it.

## The two genres

A **scorecard** is a lead instrument. It is optimised for a stranger who will give you
three minutes and no artifacts. Fixed question order, forced choice, a number, a band,
a call to action. The constraint that shapes every design decision is that it cannot
see anything about the respondent except what they type.

A **reflection skill** runs inside the reader's own agent, in the repo, board, or doc
where their work actually lives. It can ask a follow-up. It can read the roadmap. It
can say "you told me you run experiments, but the last four items on this board are
all builds — which is it?" It has no reason to keep the score.

So the conversion is not a port. It is an extraction: the scorecard's *rubric* is the
asset, and the scoring machinery is packaging that should not survive the move.

## What carries over

**The behavioural ladders are the whole point.** A well-built scorecard question does
not ask "how mature are you, 1-5." It offers three or five observable behaviours and
lets the reader recognise themselves:

> How do your AI initiatives typically get started?
> 1. Based on new tech trends or what competitors are doing.
> 3. From general business goals, but the specific problem isn't always clear.
> 5. Directly from a specific, well-understood business or customer bottleneck.

That is a rubric with evidence anchors, and it is worth more to a skill than to a quiz —
an agent that can read artifacts can *place* the organisation on that ladder instead of
asking it to self-report. Keep every ladder, verbatim, in a `references/` file. Do not
paraphrase them into vaguer language; the specificity is the value.

**Categories become dimensions.** They are already the axes of the diagnosis.

**Scale questions carry their poles.** A `scale` question's `minLabel`/`maxLabel` pair
("We stick to the plan to avoid failing" → "We pivot or kill the project immediately")
is a two-rung ladder. Same treatment.

**Band narratives become pattern names.** "AI Theater Zone," "Feature Factory Hamster
Wheel," "The Messy Middle" are diagnoses a reader recognises. Keep the name and the
`message`/`detailedFeedback` prose as *interpretation*, but detach them from the score
range — the skill names the pattern it sees, it does not compute a threshold.

**`categoryInsights` are the richest thing in the export and the most likely to be
missed.** Where a scorecard has them, each dimension carries red/amber/green prose and
three recommendations apiece. That is a ready-made per-dimension coaching layer.

## What to throw away

**The score.** A number out of 40 means something when it segments a mailing list. In a
one-on-one coaching conversation it is false precision, and it invites the reader to
optimise the number instead of the system. Name the pattern instead.

**Weight-0 questions, mostly.** These are stealth qualifiers — budget, urgency,
authority, which funnel stage — and they exist to score the *lead*, not to serve the
respondent. Drop them. The exception is the occasional one that is genuinely a good
reflection prompt ("if nothing changes for 6-12 months, what happens to the business?").
Keep those, reframed as a question rather than a multiple choice.

**Every CTA.** A skill running in someone's harness that ends by pitching a session is a
skill they uninstall. The repo convention is a single Source footer with attribution and
one link; that is the entire ask.

**Question order.** The scorecard's order is tuned for completion rate. A skill should
follow the conversation.

## What has to be added

This is what makes the skill worth building rather than linking to the quiz.

1. **Evidence over self-report.** Ask what the agent can look at — the initiative list,
   the last quarter's shipped work, the roadmap doc, the OKR page, recent PRs — and place
   the reader on the ladder from what is actually there. Where self-report and artifact
   disagree, say so. That is the single biggest thing the web version cannot do.
2. **Adaptive questioning.** One or two questions at a time, chosen from the last answer.
   Stop when the binding constraint is obvious rather than completing the set.
3. **One experiment, not a recommendations list.** Every skill in this repo ends in one
   move sized for 2-4 weeks, with a leading indicator and a stopping rule. The scorecard's
   three bullet recommendations are raw material for choosing that one move, not the output.
4. **A named uncertainty.** Say what you could not tell from what you were given.

## The house shape

Match the existing skills — `sniff-test`, `flow-metrics-self-assessment`,
`portfolio-to-product-shift-coach` are the reference implementations:

```
---
name: <slug>
description: <what it does, then "Use when ..." triggers>
metadata:
  version: 1.0.0
---

You are a <role>, <framing sentence>.

### Context          — what to ask for if not already given
### Instructions     — Phase 1 locate / Phase 2 diagnose / Phase 3 one move
### References       — the ladders file, plus source articles
### Output Format    — a short bolded list, the same shape every run
### Tone             — direct, practitioner-to-practitioner

---

## Source
```

Ladders go in `references/<name>-ladders.md` so the SKILL.md stays readable and the
rubric loads only when the conversation needs it.

## Extracting the source material

The scorecards live in the `assessments` table of the `vibe-scorecard` Supabase project,
one row per scorecard with `categories`, `questions`, and `scoring_bands` as JSONB.

Two traps:

- **The app's JSON export was lossy.** It dropped `options`, `scaleLabels`,
  `categoryInsights` and `resultsVisualizationType` — that is, it dropped exactly the
  ladders you came for. Fixed in `vibe-scorecard`; regenerate any export taken before
  that fix rather than trusting the file in the repo.
- **Option schema drifts by vintage.** Older rows use `{label, value}`, newer ones
  `{text, score}`, and `which-flow-metrics` uses `{text, value, description}`. Read all
  three or you will silently get empty ladders.

## Conversion status

| Scorecard | Disposition |
|---|---|
| `ai-traction-scorecard` | → `skills/ai-traction-self-assessment` |
| `ai-fluency-diagnostic` | → `skills/ai-fluency-self-assessment` |
| `deep-product-maturity-audit` (40q) | → `skills/product-operating-model-audit` (deep mode) |
| `product-transformation-maturity` (10q) | → same skill, short mode |
| `which-flow-metrics` | → ladders folded into existing `flow-metrics-self-assessment` |
| `ai-traction-scorecard-old` | Superseded by `ai-traction-scorecard`; not converted |
| `product-flywheel`, `product-agility-health-check` | Identical question sets; ground already covered by `portfolio-to-product-shift-coach` |
| `product-org-scorecard`, `product-organization-scorecard` | Overlapping project→product variants; folded into the POM audit |
| `okr-flywheel-scorecard` | Candidate. Overlaps `outcome-framing-coach` at the epic level and existing OKR coaching at the system level — convert only if the OKR-system angle is not already served |
| `pom-workshop-pilot` | Workshop instrument, not a standalone diagnostic |
| `founder-blind-spot-v1` | Off-brand for this repo — founder audience, not AI-impact leadership |
| `consulting-clarity-gap-analysis` | Yuval's own practice-building tool, and built on a third party's framework. Not for publication here |
