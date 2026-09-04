# ai-impact

Skills you install into your own AI agent, for the work of turning AI activity
into business impact.

By [Yuval Yeret](https://yuvalyeret.com) — AI Transformation Advisory and
Organizational AI Coaching.

## What this is

Most organizations running AI pilots have more activity than evidence. There
are demos, a committee, a few teams shipping faster, and no clear line from any
of it to a business outcome anyone would defend in a budget conversation.

These are the diagnostics and coaches Yuval uses on that problem, packaged so
your agent can run them. They ask questions rather than hand you a framework:
where the constraint actually sits, whether an initiative has enough clarity
for the stage it claims, what a starting WIP limit should be when agents write
much of the code, whether flow metrics would tell you anything you would act on.

They are meant to be run against your real situation, with your real data, in
your own tooling. That is deliberate — a hosted chatbot that answers about
Yuval is less useful than something that works inside the loop you already run.

## Install

Skills follow the standard `skills/<name>/SKILL.md` layout, so most agent
tooling picks them up directly.

```bash
git clone https://github.com/yyeret/ai-impact
```

Point your agent at the folder, or copy the skills you want into wherever your
harness keeps them — `~/.claude/skills/`, `~/.agents/skills/`, or the
equivalent. Each skill is a single Markdown file plus, for some, a `references/`
folder it loads on demand.

## What's here

**Diagnosing where you actually are**

| Skill | Use it when |
|---|---|
| `sniff-test` | An initiative is heading for a commit decision and you want to know whether its clarity matches its stage |
| `sniff-test-portfolio` | You are reading a whole board and want the patterns a single-initiative read cannot see — duplication, hidden WIP, risk balance |
| `portfolio-to-product-shift-coach` | "We do product now" is claimed, but funding and governance still run by project |
| `product-operating-model-audit` | You want to know how far the operating model has actually moved from project to product, across strategy, people, governance and the value cycle |

**Making outcomes legible**

| Skill | Use it when |
|---|---|
| `outcome-framing-coach` | Epics are written as output and nobody can say what would change if they shipped |
| `flow-coaching` | You want flow to be visible and steerable rather than reported |
| `flow-metrics-self-assessment` | Before adopting flow metrics, to decide whether they would tell you anything you would act on |
| `wip-limit-configuration-coach` | Agents write much of the code and your existing WIP limits no longer describe the system |

**AI transformation and delivery**

| Skill | Use it when |
|---|---|
| `ai-traction-self-assessment` | There is a lot of AI activity and no defensible line from any of it to a business outcome |
| `ai-fluency-self-assessment` | AI is clearly helping, the leverage has plateaued, and every session starts by re-explaining the same background |
| `agility-ai-transformation` | Building the narrative from AI activity to business impact, without AI theater |
| `yuval-ai-dlc-coach` | Coaching engineering and AI-enablement leaders through the AI development lifecycle |
| `sdd-orchestrator` | Running spec-driven development so agents work against a real spec |
| `descaling-experiment-coach` | A scaling framework was adopted with compromises that were meant to be temporary |

Several skills came from articles, and each one links back to the piece that
explains the reasoning behind its questions. Others were extracted from the scorecards
at [yeretagility.com](https://yeretagility.com) — [docs/scorecard-to-skill.md](docs/scorecard-to-skill.md)
says what carries over from a scorecard to a skill, what gets thrown away, and what has
to be added.

## Context for your agent

Yuval publishes a dossier — what he works on, how he thinks about problems, and
the boundaries on speaking for him. It lives on the site rather than in this
repo, so there is one copy and it cannot drift:

- Skill: <https://yuvalyeret.com/ai/yuval-agent-skill/SKILL.md>
- Full dossier: <https://yuvalyeret.com/ai/yuval-agent-dossier.md>
- Paste-in snippet for an existing `AGENTS.md`: <https://yuvalyeret.com/ai/yuval-agent-dossier/AGENTS.md>

## Attribution and boundaries

These skills describe how Yuval works. They do not speak as him, and their
output is not his assessment of your situation. If you want that,
[talk to him](https://yuvalyeret.com/contact/).

Where a skill builds on someone else's published work, it says so and links to
the source. `sniff-test` draws on Mark Richards' portfolio-agility work at
[Shaping Agility](https://www.shapingagility.com/).

## License

Skill content is [CC BY 4.0](LICENSE) — use it commercially, adapt it, build on
it, with attribution. Any scripts are [MIT](LICENSE-CODE).

Attribution means naming Yuval Yeret and linking back. If a skill helped, that
link is the whole ask.
