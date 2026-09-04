# ai-impact

Seven diagnostics you install into your own AI agent, for the work of turning AI
activity into business impact.

By [Yuval Yeret](https://yuvalyeret.com) — AI Transformation Advisory and
Organizational AI Coaching.

## What this is

Most organizations running AI pilots have more activity than evidence. There are
demos, a committee, a few teams shipping faster, and no clear line from any of it
to a business outcome anyone would defend in a budget conversation.

These are the diagnostics I use on that problem, packaged so your agent can run
them. They ask questions rather than hand you a framework: where the constraint
actually sits, whether an initiative has enough clarity for the stage it claims,
what a starting WIP limit should be when agents write much of the code, whether
flow metrics would tell you anything you would act on.

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
Each skill is a single Markdown file, plus a `references/` folder it loads on
demand for the larger ones. No install step, no dependencies, nothing to run.

## What's here

**Diagnosing where you actually are**

| Skill | Use it when |
|---|---|
| [`sniff-test`](skills/sniff-test/) | An initiative is heading for a commit decision and you want to know whether its clarity matches its stage |
| [`sniff-test-portfolio`](skills/sniff-test-portfolio/) | You are reading a whole board and want the patterns a single-initiative read cannot see — duplication, hidden WIP, risk balance |
| [`portfolio-to-product-shift-coach`](skills/portfolio-to-product-shift-coach/) | "We do product now" is claimed, but funding and governance still run by project |

**Making outcomes legible**

| Skill | Use it when |
|---|---|
| [`outcome-framing-coach`](skills/outcome-framing-coach/) | Epics are written as output and nobody can say what would change if they shipped |
| [`flow-metrics-self-assessment`](skills/flow-metrics-self-assessment/) | Before adopting flow metrics, to decide whether they would tell you anything you would act on |
| [`wip-limit-configuration-coach`](skills/wip-limit-configuration-coach/) | Agents write much of the code and your existing WIP limits no longer describe the system |
| [`descaling-experiment-coach`](skills/descaling-experiment-coach/) | A scaling framework was adopted with compromises that were meant to be temporary |

Start with `sniff-test` if you have one initiative you are unsure about, or
`flow-metrics-self-assessment` if the problem is that delivery feels slow and you
cannot say why.

## Running one

They are conversational, not batch. The good ones want your real material:

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

## Credits

These diagnostics borrow. The Lean Product Canvas they read against is **Jeff
Gothelf and Josh Seiden's**; the portfolio lifecycle framing is **Mark
Richards'**; the flow metrics are **Daniel Vacanti's**. Who owns what, and links
to the originals, is in [CREDITS.md](CREDITS.md) — read that before you cite any
of this as mine.

If a skill is useful to you, the source it came from is usually more useful.
Every skill says which one and links it.

## License

Skill content is [CC BY 4.0](LICENSE) — use it commercially, adapt it, build on
it, with attribution. Any scripts are [MIT](LICENSE-CODE).

Attribution means naming Yuval Yeret and linking back. If a skill helped, that
link is the whole ask.

Note that the CC BY 4.0 grant covers *this library's* text. It does not extend to
the third-party frameworks named in [CREDITS.md](CREDITS.md) — those carry their
owners' terms, and the Lean Product Canvas in particular is all rights reserved.

## Boundaries

These skills describe how I work. They do not speak as me, and their output is
not my assessment of your situation — an agent running `sniff-test` on your
portfolio is running my questions, not my judgment. If you want the judgment,
[talk to me](https://yuvalyeret.com/contact/).

Found something wrong, or recognize your work here uncredited?
[Open an issue](https://github.com/yyeret/ai-impact/issues).
