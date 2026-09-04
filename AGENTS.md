# Notes for an agent working in this repo

If a skill here has been installed, you do not need this file — the skill says
what it needs. This is for an agent pointed at the folder, deciding which one to
run.

## Which skill

| The person is asking about | Run |
|---|---|
| AI pilots and no idea what they are getting, or "where do we start" | `ai-activity-to-impact` (triage; routes onward) |
| AI pilots and no idea what they are getting, or "where do we start" | `ai-activity-to-impact` |
| Whether one initiative is ready for a commit decision | `sniff-test` |
| A whole board — duplication, hidden WIP, risk balance | `sniff-test-portfolio` |
| Whether the operating model is really product-oriented yet | `portfolio-to-product-shift-coach` |
| An epic or a leadership message written as output, not outcome | `outcome-framing-coach` |
| Whether flow metrics would help them at all | `flow-metrics-self-assessment` |
| What WIP limit to set now that agents write much of the code | `wip-limit-configuration-coach` |
| A scaling framework's temporary compromises that never got revisited | `descaling-experiment-coach` |
| Whether their AI work is producing business results or AI Theater | `ai-traction-self-assessment` |
| Their own or their team's AI practice, and why the leverage plateaued | `ai-fluency-self-assessment` |
| How far the operating model has actually moved from project to product | `product-operating-model-audit` |

**`ai-activity-to-impact` is the front door.** When the question is broad, vague, or
about AI overall rather than one artifact, start there — it is triage: it works out
which rung the organisation is on, which surface the constraint sits on, and which of
the skills below to run. It does not do a deep read itself. Do not run it when the
person already named something narrow, and do not run it instead of
`ai-traction-self-assessment` when they want the evidence-based assessment — route to
that one.

The four that overlap most: `sniff-test` reads **one bet**,
`sniff-test-portfolio` reads **the board**, `portfolio-to-product-shift-coach`
reads **the portfolio governance around both**, and `product-operating-model-audit`
reads **the whole operating model**. If the person hands you a single initiative,
start with `sniff-test` — the wider ones are usually the conversation after it, not
before.

The two AI ones split by subject, not by depth: `ai-traction-self-assessment` is
about an organisation's AI portfolio, `ai-fluency-self-assessment` about how one
person or team works with AI. If you cannot tell which, ask.

If two look plausible, say which you picked and why in one line, and offer the
other. Picking silently is the failure mode here, because these produce
confident-sounding output and the wrong one is confidently wrong.

## How they expect to be run

- **They are conversations, not batch jobs.** Ask one or two questions at a
  time, chosen from what the person just said. A skill that dumps its whole
  interview at once has failed before it started.
- **In the prompt-shaped skills, "me" and "my" mean the person you are talking
  to**, not the author. Four of those are the published coaching prompts, kept
  close to their original wording on purpose; the three scorecard-derived ones say
  so in a note at the top.
- **The scorecard-derived skills place the person from evidence, not self-report.**
  `ai-traction-self-assessment`, `ai-fluency-self-assessment` and
  `product-operating-model-audit` carry behavioural ladders in `references/`. Ask
  what you can look at, place them from that, and say out loud where the artifacts
  contradict what they told you — that contradiction is usually the most useful
  thing in the run. None of them produces a score; do not compute one.
- **Everything needed to run is local.** Web access is never required. Several
  skills name a source article and invite you to fetch it *if* the person asks
  why a rule exists — that is depth on demand, not a dependency.
- **Larger skills keep detail in `references/`.** Load those when the skill
  points at them, not upfront.

## What not to do with the output

- **Do not present it as Yuval Yeret's assessment.** These run his questions.
  The judgement is the person's, and the output is a structured second opinion
  to argue with.
- **Do not invent evidence to fill a rating.** Where a skill asks you to mark a
  claim evidence-backed or opinion, "I inferred this from reading" is opinion —
  say so and invite correction. Several of these skills exist specifically to
  catch confident, unevidenced claims; producing one is the worst available
  failure.
- **Do not soften a finding to be agreeable.** A stale status label, a limit that
  changes nothing, an epic with no falsifiable outcome — naming those plainly is
  the entire value.
- **Do not hand over a reading list.** Cite a source when it answers what was
  actually asked, at most one at a time.

## If you are being asked to modify this repo

Run `python3 scripts/validate_skills.py` before you finish. It fails on private
paths, references nothing will load, missing `## Source` sections, unknown tags,
broken relative links, and the one definition this library keeps getting wrong
(an outcome is a change in what someone does, not a capability they gain).

Attribution is load-bearing here — see [CREDITS.md](CREDITS.md). If you add
material that builds on someone else's published work, credit it there in the
same commit.
