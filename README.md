# ai-impact

**Scaling AI activity into business impact — as thinking tools your own AI agent
runs with you, on your real portfolio, in the tooling you already use.**

Some are reflection: noticing what hardened into a constraint while nobody was
looking. Some are working a number through until it fits your system instead of a
formula. Some are diagnosis: reading an initiative's clarity against the stage it
claims. All of them ask rather than answer.

By [Yuval Yeret](https://yuvalyeret.com) — AI Transformation Advisory and
Organizational AI Coaching.

## The problem these exist for

Most organizations running AI pilots have more activity than evidence. There are
demos, a committee, a few teams shipping faster, and no clear line from any of it
to a business outcome anyone would defend in a budget conversation.

The gap is rarely the technology. It is that nobody can say which initiative is
actually ready to commit to, where the constraint has moved now that code is
cheap, or what would have to change for the next quarter's spend to be
defensible. Those are answerable questions. They just require someone to ask them
properly, against your real material, and to not flinch at the answer.

That asking is what these skills do — and asking well is most of the work. A good
run is closer to a hard conversation with someone who knows your context than to
a report landing in your inbox.

## Why this is called ai-impact

Because impact is the third rung, and most organizations stall on the first two.

**Activity** is tool access, pilots, training, hackathons, a committee. Real
motion, and a reasonable place to start. It turns into theater when it plateaus
there and the organization starts celebrating the activity itself — seats
provisioned, people trained, pilots counted — because those are the easy things
to measure.

**Output** is a group, usually engineering, visibly shipping more. Better than
activity, and still frequently invisible in the business. Revenue per person has
not moved. Nothing downstream got easier.

**Impact** is when the constraint *across the business* got attacked and a
result changed. Not the place AI was easiest to apply — the place the outcome was
actually waiting.

There is no single move that gets you from the first rung to the third. It takes
attention to how work actually flows, to the forces pulling on the organization,
to the technology, and to the structure, the dynamics, and the hearts and minds
around it — all at once. Anyone selling a silver bullet is selling something.

That is why this is a library rather than a tool. Each skill works one of those
surfaces, and [`ai-activity-to-impact`](skills/ai-activity-to-impact/) is the
front door: it works out which surface is actually in your way, then hands you to
the skill for it. If it turns out none of them fits — the constraint is in
hiring, or pricing, or data access — it says so, which is better information than
a forced fit.

## The job you are hiring this for

Pick the row that sounds like your week. If none of them do, this probably is not
for you, and that is a fine outcome to reach in thirty seconds.

| When you are stuck on | Run | You end up with |
|---|---|---|
| "We have pilots, licences and enthusiasm, and no idea what we are getting" | [`ai-activity-to-impact`](skills/ai-activity-to-impact/) | Whether you are at activity, output or impact; the constraint the result is actually waiting on; and which of the skills below is the one to run |
| "We commit budget in three weeks and I don't know if this initiative is really ready" | [`sniff-test`](skills/sniff-test/) | Where clarity is thin *for the stage it claims*, whether the status label survives contact with the evidence, and the one conversation to have before the money moves |
| "I inherited this board and I can't see the patterns in it" | [`sniff-test-portfolio`](skills/sniff-test-portfolio/) | Duplicated bets, hidden WIP, whether the risk balance is intentional, and what to raise at the next review |
| "We say we're product-led but funding still runs by project" | [`portfolio-to-product-shift-coach`](skills/portfolio-to-product-shift-coach/) | Where you actually sit, which of five gaps is binding, and one experiment for the next month |
| "Our epics are written as output and nobody can say what would change if they shipped" | [`outcome-framing-coach`](skills/outcome-framing-coach/) | Each item classified, the prescriptive verbs flagged, and rewrites stated as behaviour someone can falsify |
| "Delivery feels slow and I can't say why" | [`flow-metrics-self-assessment`](skills/flow-metrics-self-assessment/) | Whether flow metrics would tell you anything you would act on — and which one to start with, or a clear no |
| "Agents write most of our code and our WIP limits stopped meaning anything" | [`wip-limit-configuration-coach`](skills/wip-limit-configuration-coach/) | Starting numbers derived from your actual constraint, with the arithmetic shown and the traps named |
| "We adopted a scaling framework and its temporary compromises never got revisited" | [`descaling-experiment-coach`](skills/descaling-experiment-coach/) | Which concession hardened into a constraint, and one small experiment against it |
| "There is a lot of AI activity here and no defensible line from any of it to a business outcome" | [`ai-traction-self-assessment`](skills/ai-traction-self-assessment/) | Where the evidence — not the story — puts you on four dimensions, which one is binding, and one experiment against it |
| "AI is clearly helping me and the leverage has plateaued" | [`ai-fluency-self-assessment`](skills/ai-fluency-self-assessment/) | Which rung is actually binding across automation, augmentation, agency and context, and one habit change with an artifact at the end of it |
| "We say we do product now, and I want to know how far that is actually true" | [`product-operating-model-audit`](skills/product-operating-model-audit/) | Where you sit across strategy, people, governance and the value cycle, the shape rather than the average, and the gravity your one experiment will meet |

**The common shape:** each one ends in a conversation to have or an experiment to
run in the next two to four weeks, with a leading indicator you could actually
watch. None of them ends in a score.

## How they work

They are mostly questions, run as a conversation — your agent asks one or two at
a time and follows what you say, rather than dumping a survey. What that
conversation is doing varies:

- **Reflection.** `descaling-experiment-coach` and `portfolio-to-product-shift-coach`
  mostly help you see your own situation clearly — which compromise hardened, where
  you actually sit — before anyone proposes anything.
- **Thinking a thing through.** `wip-limit-configuration-coach` deliberately
  refuses to hand you a formula. It walks you to a number that fits your system and
  makes you able to defend it, which is the part that survives after the run.
- **Diagnosis.** `sniff-test`, `sniff-test-portfolio`, `ai-traction-self-assessment`
  and `product-operating-model-audit` do read your material and come back with
  findings — the closest thing here to an assessment, and the traction one
  deliberately reads what you shipped rather than how you describe yourselves.
- **Triage.** `ai-activity-to-impact` does none of the above. It works out which
  rung you are on and which surface the constraint sits on, then hands you to the
  skill built for it. Minutes, not an afternoon.

Most runs are some of each. Some carry a rubric behind the questions, because you
cannot judge clarity against a stage without saying what the stages are. Where they do, they say the shape is one shape and not
the shape, and tell you to map it onto whatever your organization actually calls
things.

They are meant to run against your real situation, with your real data, in your
own tooling. That is deliberate — a hosted chatbot that answers questions about
me is less useful than something that works inside the loop you already run.

**What they are not:** a maturity model, a scoring rubric to send upward, or a
substitute for knowing your own organization. Every one of them can be argued
with, and the good runs usually involve arguing.

## Install

**As a Claude Code plugin:**

```
/plugin marketplace add yyeret/ai-impact
/plugin install ai-impact@ai-impact
```

**Anywhere else.** Skills follow the standard `skills/<name>/SKILL.md` layout, so
most agent tooling picks them up directly:

```bash
git clone https://github.com/yyeret/ai-impact
```

Point your agent at the folder, or copy the skills you want into wherever your
harness keeps them — `~/.claude/skills/`, `~/.agents/skills/`, or the equivalent.
Each skill is a `SKILL.md`, plus for some a `references/` folder it loads on
demand and an `agents/` folder holding config for a specific host (there is one,
for an OpenAI-style agent). No install step, no dependencies, nothing to run.

**Three shapes in here, deliberately.** `sniff-test`, `sniff-test-portfolio` and
`outcome-framing-coach` are structured skill documents. Four —
`portfolio-to-product-shift-coach`, `flow-metrics-self-assessment`,
`wip-limit-configuration-coach`, `descaling-experiment-coach` — are the coaching
prompts published alongside their articles, kept close to that wording on purpose,
so what you install matches what you can read on the site and use in a plain chat
window. The three `*-self-assessment` and `*-audit` skills were extracted from the
scorecards at [yeretagility.com](https://yeretagility.com): they carry the
scorecard's behavioural ladders in `references/`, but drop the score and ask your
agent to place you from your own artifacts instead.
[docs/scorecard-to-skill.md](docs/scorecard-to-skill.md) records what carries over
from a scorecard to a skill, what gets thrown away, and what has to be added. If
they read differently from each other, that is why.

**Before pointing one at anything confidential**, read [SECURITY.md](SECURITY.md)
— short version: this repo runs nothing and sees nothing, but your agent will
send whatever you give it to your model provider, and every skill also works as
a plain interview with no data access at all.

## Where to start

**`ai-activity-to-impact` if you are not sure** — it is triage, and it exists to
work that out and hand you on in minutes. Otherwise go straight to the narrow one:
`ai-traction-self-assessment` if the honest answer to "how is the AI programme
going" is a list of pilots, `sniff-test` for a single initiative you are unsure
about, `outcome-framing-coach` for the cheapest possible first run (paste a dozen
epic titles and see what comes back), or `flow-metrics-self-assessment` if delivery
feels slow and you cannot say why.

The four that overlap: `sniff-test` reads **one bet**, `sniff-test-portfolio`
reads **the board**, `portfolio-to-product-shift-coach` reads **the portfolio
governance around both**, and `product-operating-model-audit` reads **the whole
operating model**. Start with the narrowest one that fits — the wider
conversations usually come after it, not before.

If you are pointing an agent at this folder rather than installing,
[AGENTS.md](AGENTS.md) is the routing map, plus how the skills expect to be run.

## Running one

They are conversational, not batch, and they cost about what a good 1:1 costs:
ten to twenty minutes for most, longer for `wip-limit-configuration-coach`, which
works through a fifteen-question interview before it computes anything. The good
ones want your real material:

```
Use the sniff-test skill on the "Unified Billing" epic.
The board is in Confluence at <link>; the canvas and last sponsor update are there.
I think it's in Plan/Commit but I'm not sure that's still true.
```

The skill will verify the stage against the evidence before it rates anything,
because a status label is the thing most likely to be stale. With thin input it
will ask you for context first and tell you the run will be noisy — that is
working as intended, not a failure.

Give it less and it still runs:

```
Use the outcome-framing-coach skill on these twelve epic titles: <paste>
```

**Four things that make a run worth the time:**

1. **Point it at the system of record, not a summary you wrote.** The stale
   status label, the roadmap with no confidence range, the eleven features all
   sitting in "not started" — those are the findings, and they only exist in the
   real material. A tidy briefing hides exactly what you want found.
2. **Argue with it.** These produce confident-sounding output from whatever you
   fed them. When a rating is wrong because the evidence lives somewhere the agent
   never saw, say so and re-run that dimension — the good sessions are half
   correction.
3. **Answer honestly about intent.** Several skills ask whether you want to
   preserve current behaviour or change it. Answer "change it" and mean it, or
   you will get a number that ratifies what you already do.
4. **Stop at the experiment.** Each one ends in one thing to try in two to four
   weeks with an indicator to watch. That is the deliverable. A run that produces
   a table and no next move has failed, and the skills say so themselves.

**No web access, or working on something confidential?** Every skill runs as a
plain interview with no data access at all — you answer from material the agent
never sees. You lose `sniff-test`'s evidence-based stage check, which is the most
valuable thing it does; the rest of the read still works. See
[SECURITY.md](SECURITY.md) for what does and does not leave your building.

**Want to see what comes back before you spend the time?** Two full runs, both on
made-up teams, each showing what went in, what came out, how long it took, what it
changed, and what it got wrong:

- [A `sniff-test` run](examples/sniff-test-worked-example.md) — one initiative, four minutes of reading.
- [A `wip-limit-configuration-coach` run](examples/wip-limit-worked-example.md) — the long one, 35 minutes, including where the skill contradicts its own default and why.

## Credits

These skills document and make available practices and perspectives I use in my work day in and day out helping leaders shift AI from activity to impact, standing on the shoulders of giant principles, bodies of work, and thought leaders. 
If a skill is useful to you, the source it came from is usually more useful.
Every skill says which one and links it.
Consider part of this repository's value to be a librarian for your AI activity, to impact research and action. 
You can find more details in [CREDITS.md](CREDITS.md). 

## License

Skill content is [CC BY-SA 4.0](LICENSE) — use it commercially, adapt it, build
on it, with attribution, and **share your adaptations under the same licence**.
Any scripts are [MIT](LICENSE-CODE).

Attribution means naming Yuval Yeret and linking back. If a skill helped, that
link is the whole ask.

**What ShareAlike actually asks of you.** It engages when you *share* — publish a
fork, ship a modified version, put an adapted skill in a public repo or a product.
Then that adaptation carries CC BY-SA 4.0 too, so the next person gets what you
got. It does **not** engage on private use: running these against your portfolio,
editing them for your own team, folding the questions into an internal playbook
you never publish — none of that is sharing, and none of it triggers anything.
Output from a run is yours; it is not an adaptation of the skill.

The point is not to restrict you. It is that these questions were built on other
people's published thinking, and the same openness should survive the next hop.

The grant covers *this library's* text only. It does not extend to the
third-party frameworks named in [CREDITS.md](CREDITS.md) — those carry their
owners' terms, and the Lean Product Canvas in particular is all rights reserved,
which is exactly why these skills reference it rather than reproduce it.

## Boundaries

These skills describe how I work. They do not speak as me, and their output is
not my assessment of your situation — an agent running `sniff-test` on your
portfolio is running my questions, not my judgment. If you want the judgment,
[talk to me](https://yuvalyeret.com/contact/).

Found something wrong, or recognize your work here uncredited?
[Open an issue](https://github.com/yyeret/ai-impact/issues).
