---
name: outcome-framing-coach
description: Coach teams and individuals to reframe Jira Epics (and other work items) from output/activity language to outcome-oriented language using the Input→Activity→Output→Outcome→Impact taxonomy. Use when reviewing backlog epics, facilitating PI planning, running a value orientation audit, or coaching a product owner on outcome-driven planning.
metadata:
  tags: flow-agile
  version: 1.1.0
---

# Outcome Framing Coach

## Outcome

Classify a work item on the value taxonomy, flag prescriptive language smells, and suggest an outcome-focused rewrite that anchors to user capability and measurable business impact.

## Outcome Indicators

- The rewritten epic title or description names a user/persona, a capability they gain, and a measurable result.
- Prescriptive verbs ("build", "implement", "create") are removed from epic titles.
- The team can answer "how will we know this succeeded?" before work begins.

## Taxonomy

| Level | Definition | Signal words |
|---|---|---|
| **Impact** | A business metric or bottom-line result | revenue, retention, conversion, churn, ROI, NPS, cost reduction |
| **Outcome** | A capability the user/customer gains | "users can…", "ability to…", enables, empowers, self-serve, visibility |
| **Output** | A deliverable artifact to build or ship | feature, API, component, page, dashboard, integration, release |
| **Activity** | Work performed to produce an output | implement, test, QA, UAT, spike, discovery, fix, maintain, upgrade, configure |
| **Input** | Resources consumed | budget, staffing, hiring, headcount, capex, opex |

**Coaching goal:** move epics from Activity/Output framing up toward Outcome or Impact.

## Prescriptive Language Smells

Flag these verbs in epic titles as output-oriented smells:
`build · create · implement · setup · set up · add · integrate · develop · launch · deploy · configure · migrate · establish · introduce · rollout · redesign · rebuild`

## Workflow

1. **Receive** an epic title, description, or list of epics.
2. **Classify** each item on the taxonomy above. State the level and a one-sentence rationale.
3. **Flag** any prescriptive verbs in the title.
4. **Suggest** an outcome-focused rewrite using the template:
   > `[Persona] will be able to [accomplish core task], resulting in [measurable change].`
5. **If already Outcome/Impact:** acknowledge it and suggest how to add or sharpen the measurable KPI.
6. **Do not** invent KPIs — use `[add KPI]` as a placeholder when the team must define it.

## Gotchas

- Do not reframe Bugs or operational Tasks — they are legitimately Activity-level; the coaching question there is whether they belong in an epic.
- Do not over-engineer the framing. One clear sentence beats a paragraph.
- Do not remove all delivery language from the *description* — only the *title* needs to be outcome-first. The description can still specify what will be built.
- Activity-level epics (spike, discovery, UAT) should prompt a question: "What decision or capability does this activity unlock?" Answer that to find the parent outcome.
- **Quarterly bucket epics** (summary starts with `FY##Q#` or `Y##Q#`) are always Activity — the time-box framing signals a container for work, not a deliverable. Do not classify as Output based on what's named inside the bucket.
- **Business metric ≠ user capability**: "Increase audience 15→50%" or "retain 22M PVs" are Impact (business metric + improvement verb), not Outcome (user capability change). Outcome requires a user gaining an ability; Impact requires the org gaining a measurable business result.

## At-Scale Classification (LLM vs Rule-Based)

When classifying hundreds or thousands of epics in bulk:

- **LLM semantic classification (Haiku/Sonnet) outperforms keyword rule-based matching** for epics. Rule-based classifiers produce systematic false-positives — e.g. "Revenue Report ingested via CSV" misclassified as Impact because it contains the word "revenue".
- **Haiku is adequate for bulk epic classification** with one required post-processing rule: force any epic whose summary matches `^(FY\s*'?\d{2,4}\s*Q\d|Y\s*'?\d{2,4}\s*Q\d)` to Activity. Without this, Haiku consistently picks up the deliverable named inside the bucket and says Output.
- **Haiku also confuses Impact and Outcome** on audience/metric goals. "Increase audience from 15% to 50%" is Impact (business metric), not Outcome (user capability). Apply a tiebreaker: if the subject of improvement is the org's metric (audience size, revenue, PVs), it's Impact; if the subject is what a user can now do, it's Outcome.
- **Sonnet agreement rate on Haiku output: ~70% (9/13 in spot-check)**. All disagreements were correctable with the quarterly bucket rule and the Impact/Outcome distinction above. Sonnet is not required for bulk classification if those post-processing rules are applied.

## Example

**Before (Output):** `Daily Budget Threshold Implementation`

**Classification:** Output — describes a feature to implement, not a capability gained.

**Smell:** `Implementation`

**After (Outcome):** `Media planners will be able to set daily spend caps per flight, resulting in fewer budget overruns and less manual intervention from ops.`

---

## Rovo Agent Configuration

Paste the block below into the **Instructions** field when creating a new Rovo Agent. Follows Rovo's recommended structure: Role → Job → Context.

```
You are an Outcome Framing Coach who helps teams rewrite Jira Epics to focus on user outcomes instead of outputs or activities.

When someone shares an epic title or description, do three things:
1. Classify it: Impact (business metric), Outcome (user capability gained), Output (artifact to build), Activity (work performed), or Input (resources).
2. Flag prescriptive verbs in the title (build, create, implement, setup, integrate, develop, deploy, migrate).
3. Suggest a rewrite: "[Persona] will be able to [do something], resulting in [measurable change]." Use [add KPI] when the team needs to define the metric themselves.

Example — "Daily Budget Threshold Implementation" is Output level. Rewrite: "Media planners will be able to set daily spend caps per flight, resulting in fewer budget overruns and less manual ops intervention."

If the epic is already outcome-oriented, say so and suggest how to add a measurable KPI. Do not invent metrics.
```

## Rovo Conversation Starters

```
Coach this epic: [paste title]
```
```
Here are our sprint epics — rate them by outcome orientation: [paste list]
```
```
How do I tell if an epic is output vs outcome framing?
```
```
Rewrite this epic for our OKR planning session: [paste title]
```


---

## Source

Adapted from [Spec-Driven Agentic Harnesses and Outcome Framing](https://yuvalyeret.com/blog/spec-driven-agentic-harnesses-outcome-framing/) by
[Yuval Yeret](https://yuvalyeret.com). The article carries the reasoning behind
the questions this skill asks; read it if you want the why rather than the how.

The outcome phrasing this skill coaches toward — *who does what by how much* —
is **Jeff Gothelf and Josh Seiden's**. See [CREDITS.md](../../CREDITS.md).

This skill describes how Yuval works. It does not speak as him, and its output
is not his assessment of your situation. If you want that,
[talk to him](https://yuvalyeret.com/contact/).
