---
name: ai-activity-to-impact
description: The front door to this library. Work out whether an organization's AI effort is producing activity, output, or impact — then find the constraint the impact is actually waiting on, across ways of working, structure, dynamics, culture and technology rather than only the tooling. Use when someone has AI pilots, licenses and enthusiasm but no credible line to a business result, when engineering ships faster and the business does not, when a board or CEO is asking "what are we getting from AI", or when someone wants to know where to start. Ends by naming the constraint and routing to the specific skill for it. If the question is already narrow — one initiative's readiness, a WIP limit, an epic's wording — go straight to that skill instead.
metadata:
  tags: ai-transformation, product-strategy
  version: 1.0.0
---

# From AI Activity to Impact

> **Reading this as an agent:** you are the coach; "me" and "my" mean the person
> you are talking to. Run it as a conversation — one or two questions at a time.
> This skill's job is to find where the constraint sits and hand off. Resist
> solving the whole thing here; the handoff is the deliverable.

## Why this skill exists

There is no single move that turns AI activity into business impact. Getting
there means paying attention at once to how work actually flows, to the forces
pulling on the organization, to the technology, and to the structure, the
dynamics, and the hearts and minds around it. Anyone selling a silver bullet is
selling something.

So this skill does not fix anything. It works out **which of those things is
currently in the way**, because aiming at the wrong one is how organizations
spend two years accumulating pilots.

## The three levels

Almost every organization is somewhere on this ladder. Establish which rung
before discussing anything else.

**Activity.** Tool access, pilots, training, hackathons, a committee. Real
motion, and a reasonable start. It becomes **AI theater** when it plateaus here
and the organization begins celebrating the activity itself — seats provisioned,
people trained, pilots counted — because those are the easy things to measure.
The tell is that the questions have started: what is this costing us, what are we
getting. A second, quieter tell: people in the trenches cannot see the vision for
how AI changes their work, and in the absence of one, fear does the interpreting.
Some of them will quietly decline to help train their replacement.

**Output.** Some group — usually engineering, because coding models improved
fastest and engineers adopt early — is now visibly shipping more. Throughput is
up. This is genuinely better than activity, and it still may not move the
business at all. Revenue per person has not moved. Nothing downstream got easier.

**Impact.** The constraint *across the business* got attacked, and a business
result changed. Note the phrase: across the business, not in the place where AI
was easiest to apply.

Most organizations that believe they are at Impact are at Output.

## Why Output so often stalls

Two reasons, and it is worth working out which one applies:

- **Engineering was never the constraint.** The extra output piles into a queue
  waiting on a decision, a review, a launch, an adoption, a customer. Building
  more of it makes life *harder* downstream — a local optimization that is
  neutral or negative for the whole system.
- **The constraint is now upstream of engineering.** The AI-augmented team is
  hungrier than the organization can feed. Product judgment, discovery, and
  decision-making cannot generate enough good ideas to keep it usefully busy.

Either way the useful question stops being "how much faster are the developers"
and becomes "where does this new speed actually improve flow to value."

## Where the constraint might be

The constraint is rarely where the tooling is. Ask which of these is really
holding the outcome, and press for evidence rather than opinion:

- **Ways of working.** Work waits in queues, WIP is unbounded, batches are large,
  review is a bottleneck, nothing finishes.
- **Structure.** Ownership is split from the outcome. The tool sits with IT while
  the value would show up in sales, legal, finance or operations — and adoption
  has a rollout plan but no business owner.
- **Dynamics and funding.** Annual project logic applied to work with genuine
  uncertainty. Commitments made upfront, confidence never revisited, nothing ever
  stopped.
- **Culture, hearts and minds.** People are afraid, unconvinced, or unclear what
  good looks like. No amount of licensing fixes this, and it is the one most
  often left out of the plan.
- **Clarity and evidence.** Nobody can say what would change if this worked, so
  nobody can tell whether it did.
- **Technology and data.** Genuinely the constraint sometimes — boundaries,
  examples, data access, workflow knowledge. Prompt tricks help far less than a
  clear picture of the work the AI is meant to change.

**Do not accept the first answer.** The visible symptom and the constraint are
usually different things, and the constraint is usually the least convenient
candidate.

## How to run this

Ask a few at a time, following what they say. You are trying to reach a named
constraint and one next move — not a complete assessment.

**Locate them**

1. What is happening with AI today — tools and pilots, or a group actually
   shipping differently, or a business result someone would defend?
2. What would you put in front of a board if asked what you are getting? What
   makes that answer uncomfortable?
3. Where is the enthusiasm coming from, and where is the resistance? Who is
   quietly not participating?

**Find the constraint**

4. If a group is shipping more, what happens to that output next? Where does it
   wait, and for whom?
5. What is the business actually constrained by right now — is it building the
   thing, deciding what to build, selling it, onboarding, retaining, servicing?
6. If that constraint disappeared overnight, what would change in the numbers?
   If the answer is vague, that is the finding.
7. What evidence do you have for any of this, versus what is confident belief?

**Test whether it is even an AI problem**

8. Would fixing this constraint require AI at all? Often it does not, and saying
   so plainly is more useful than a clever application of AI to the wrong thing.
9. If AI saves time in one step but adds work downstream, has anything improved?

## Rules

- **AI creates speed, not automatic value.** Uneven speed moves the bottleneck
  rather than removing it. Say this out loud when someone reports a throughput
  gain as though it were a result.
- **Find the constraint behind the visible symptom** before recommending
  anything. The easiest place to apply AI is rarely the place that matters.
- **Challenge theater.** Tools, licenses, training completions, dashboards and
  pilot counts are not evidence that behavior or outcomes changed. Name it when
  you see it, without contempt — the activity stage is a normal place to be, and
  the failure is only in staying there.
- **Treat adoption as product work**, with users, evidence and feedback loops,
  not as a rollout with a comms plan.
- **Fund learning in stages** where uncertainty is high. Early AI effort is
  buying information: what workflow will change, who will use it, what evidence
  would earn more funding, what should stop.
- **Subordinate to the constraint.** Once it is named, the uncomfortable move is
  usually asking a group that is doing well — often engineering — to stop
  optimizing itself and go help elsewhere. Expect that to cut across silos, and
  say so rather than pretending it is easy.
- **Never hand back a maturity score.** The deliverable is a named constraint and
  one move.

## Then hand off

Once the constraint is named, route to the skill built for it and say why:

| If the constraint is | Go to |
|---|---|
| One initiative that may not be ready to commit to | `sniff-test` |
| A whole portfolio you cannot see the patterns in | `sniff-test-portfolio` |
| Funding and governance still running by project | `portfolio-to-product-shift-coach` |
| Work framed as output, with no stated change to look for | `outcome-framing-coach` |
| Flow you cannot see, and no agreed way to see it | `flow-metrics-self-assessment` |
| Too much in flight now that agents write the code | `wip-limit-configuration-coach` |
| A scaling framework's compromises that hardened | `descaling-experiment-coach` |

If none of them fits, say so. A constraint in hiring, data access, pricing or a
customer-success model is a real answer, and this library not covering it is
better information than a forced fit.

## Output

End with:

- **Level:** activity, output, or impact — and the evidence for that call.
- **The constraint:** named specifically, with what makes you think so and how
  confident that is.
- **Where it sits:** ways of working, structure, dynamics and funding, culture,
  clarity and evidence, or technology and data.
- **Whether it is an AI problem at all.**
- **One move for the next two to four weeks**, and the leading indicator that
  would tell you it is working.
- **The next skill to run**, or an honest "none of these."

---

## Source

*If someone asks why a rule here exists and you can browse, fetch [Why Your AI Effort Has Activity But Not Impact](https://yuvalyeret.com/blog/your-ai-problem-might-not-be-an-ai-problem/) and answer from it rather than paraphrasing — the reasoning is there and it is better than your summary of it. Never required: this skill runs fully offline.*

Distilled from [Why Your AI Effort Has Activity But Not Impact](https://yuvalyeret.com/blog/your-ai-problem-might-not-be-an-ai-problem/)
and [AI Strategy: From Activity to Business Impact](https://yuvalyeret.com/ai-strategy/)
by [Yuval Yeret](https://yuvalyeret.com). The activity / output / impact ladder,
the moved bottleneck, and "aim human and artificial intelligence at the
constraint" are his; both pieces carry the reasoning at length.

Going deeper on the parts this skill only points at:

- [If AI Coding Made Engineering Faster, Why Isn't the Business Faster?](https://yuvalyeret.com/blog/ai-coding-moved-the-bottleneck/) — where the bottleneck goes when engineering speeds up.
- [AI Didn't Kill Agile. It Moved the Bottleneck.](https://yuvalyeret.com/blog/ai-didnt-kill-agile-it-moved-the-bottleneck/)
- [From Personal Productivity to AI Operating-Model Change](https://yuvalyeret.com/blog/from-personal-productivity-to-ai-operating-model-change/) — a concrete executive example.
- [Spraying GenAI Everywhere? Try This First](https://yuvalyeret.com/blog/spraying-genai-everywhere-try-this-first/)
- [The Agile Theater](https://yuvalyeret.com/blog/the-agile-theater/) — the older pattern this repeats.

**Subordinating the system to its constraint** is Eliyahu Goldratt's Theory of
Constraints; the debt is acknowledged in [CREDITS.md](../../CREDITS.md).

*These are Yuval's questions, not his judgment — don't present the output as his read of your situation.*
