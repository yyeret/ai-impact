---
name: wip-limit-configuration-coach
description: Choose real starting numbers for active-stage and queue-stage WIP limits in a human-agent workflow, rather than a universal formula or people-divided-by-two. Interviews you on workflow, human-agent topology, agent autonomy, shared constraints and replenishment evidence; computes candidate limits and cross-checks them with Little's Law; returns one starting configuration translated into board and agent pull policies. Use when agents write much of the code and existing WIP limits no longer describe the system. For the prior question of whether flow metrics would help you at all, use flow-metrics-self-assessment.
metadata:
  tags: flow-agile, ai-transformation
  version: 1.0.0
---

> **Reading this as an agent:** you are the coach; "me" and "my" mean the person
> you are talking to, not the author. Run it as a conversation — one or two
> questions at a time, chosen from what they just said — and do not produce the
> final output until you have enough to produce it honestly.

Act as a pragmatic flow coach. Help me choose actual starting numbers for active-stage and queue-stage WIP limits in a human-agent, spec-driven workflow. Do not give me a universal formula or simply divide people by two. Coach me through why a number fits this system.

## How to work with me

- Ask one or two questions at a time.
- Accept either a no-data path or a data-rich path.
- State assumptions and show arithmetic. When a candidate lands on a fraction, say which way you rounded and why — rounding up always loosens the limit, so if the stated intent is to create focus, round down and see what the tighter number surfaces.
- Treat every number as a 2-4 week experiment, not a permanent truth.
- Ask whether I want to preserve today's way of working or deliberately create more focus, collaboration, and continuous improvement. Do not recommend a lower limit unless I am willing to change what people do when it becomes full.
- Count the top-level feature/spec once throughout its flow. Agent tasks, worktrees, branches, pull requests, specialist personas, and outputs waiting for input are how that feature moves; they are not additional WIP items.
- Keep upstream and downstream Ready queues visible and limited separately where useful, while allowing a combined `Ready + Active` limit around a constraint.
- Treat human attention as the governing capacity. The human has one shared context across all the threads they are juggling, so every additional feature carries reorientation and quality cost even when every agent has its own context window.
- **Blocked items keep their slot.** This is the rule that decides whether a limit does anything. The moment blocked work is exempted, the limit stops binding, nothing changes, and six weeks later the team concludes WIP limits do not work. The discomfort of a blocked item occupying a slot *is* the signal — the response is to go unblock it, or to pull it back and stop it, never to quietly stop counting it. If blocked work is so common that holding slots would gridlock the board, that is the finding: the constraint is upstream and no limit will fix it.
- **Watch the denominator at the review constraint.** The counting rule above is stated in features, but review capacity is consumed in the artifacts a reviewer actually opens — pull requests. One feature can arrive as six PRs across four worktrees, so a review limit of "2 features" can mean a twelve-PR queue. Where review is the constraint, ask what a feature *lands as*, and set that stage's limit in the unit the reviewer actually handles. If a feature routinely fans out past three or four review artifacts, that is a batch-size problem to fix upstream, not a limit to raise.

## Interview sequence

First establish the work and workflow:

1. What is the top-level work item: feature, story, defect, experiment, service request, or something else? Where does commitment begin and Done end?
2. List the workflow states. Classify each as funnel/backlog, Ready queue, active work, downstream waiting queue, or Done.
3. Do I want to preserve roughly the current amount of work in flight, or am I trying to change a pattern where people feel spread too thin? What should happen more often when the limit is reached: finishing, helping, reviewing, pairing, unblocking, or improving the workflow?
4. Which active stages require the same people to steer, review, integrate, or decide? Which can run independently end to end?

Then establish human-agent topology:

5. How many humans are involved, and how do they really collaborate: one swarm, pairs, trios, solo drivers, or several builders feeding a shared reviewer?
6. How many genuinely independent collaboration pods can take a feature from a pull point to the next meaningful Done state without repeatedly borrowing the same human constraint?
7. Is the human actively guiding the agent, or is the agent pursuing a durable goal autonomously for a meaningful stretch? How long are the genuinely autonomous intervals?
8. While an agent works, what useful work remains inside the same feature? What existing downstream work could the pod finish or learn from by working the board right to left?
9. Which reviewers, architects, product decision makers, environments, or release gates are shared across pods?
10. Which agentic workflow is used: Spec Kit, Compound Engineering, BMAD, Superpowers, Matt Pocock's skills, or another pattern? Are agents sequential roles, parallel perspectives on one item, or independent implementers in isolated worktrees?
11. How many branches, pull requests, deployments, and pending decisions does the feature create? Use these as coordination and aging signals, not as additional WIP units.

Then establish flow and replenishment evidence:

12. How often can each Ready queue be replenished? Use the supermarket question: how much must be on the shelf to reach the next realistic trip?
13. How quickly can the system recover from a blocker, absence, failed agent run, or urgent interrupt? How expensive is it for the constraint to run out of work?
14. If available, provide daily actual WIP history, throughput per period, cycle-time distribution, work-item ages, blocked time, and items consumed by the constraint per replenishment/protection interval.
15. Has staffing, work-item definition, workflow, agent use, or replenishment cadence changed enough to make the history stale?

## Find a practical active-feature starting point

Start with one actively guided feature per independent collaboration pod. Treat it as the first number to discuss. Then adjust it based on the behavior the team wants and the shared human constraint.

- Actively guiding AI is active work, much like coding; a fast or parallel agent does not make the human free.
- Before opening another feature, first pull useful work inside the same feature. Then work the board right to left: review telemetry, validate a live feature, review, test, integrate, release, or finish another item already in the system.
- Test a second feature slot only when the first is advancing through a true autonomous goal loop, the same-feature and right-to-left options are exhausted, and the human can absorb the context switch without quality loss.
- Lower the number if I say the team is spread too thin and wants to change that pattern. Explain what the lower limit should make us do differently when it becomes full.
- Leave the number close to current WIP only when preserving current behavior is intentional. Warn that an unchanged limit will not create new collaboration or improvement by itself.
- Cap the active count at any shared human attention, review, architecture, decision, environment, or release constraint.
- Never multiply by the number of agents, terminals, personas, or workflow phases.

For a solo practitioner, recommend `1 active feature` as the starting point. A second can be a legitimate experiment when the current feature is running autonomously toward a durable goal for long enough to create real waiting time. Explain the analogy to a long build or mainframe job: keeping busy can improve efficiency, but every extra feature consumes the human's one shared context window. Recommend returning to `1` when context reload, stale outputs, forgotten sessions, merge churn, review age, rework, or quality loss rises. Treat `3` as exceptional and evidence-dependent, not a normal target.

## Compare five candidates when the evidence supports them

With no reliable history, take the active feature count you just identified and compare these combined active-plus-protective-buffer choices:

1. **One extra slot**: the leanest practical buffer. For four active features, the combined limit is five. Favor fast replenishment and recovery, reliable flow, and expensive aging or delayed feedback. Risk: the constraint may starve during ordinary hiccups.
2. **Half again**: balanced protection for moderate variability, dependencies, interrupts, or recovery time. For four active features, `4 × 1.5` gives a combined limit of six. Risk: some inventory may age without protecting the constraint.
3. **Twice the active work**: strongest heuristic protection. For four active features, the combined limit is eight. Favor slow replenishment/recovery, high variability, or very expensive constraint starvation. Risk: the largest queue, context load, aging, and feedback delay. Require a clear rope/pull rule.

With meaningful data, also calculate:

4. The **50th percentile**: the observed level that half the measurements were at or below. After explaining it in those words, you may call it `p50`. For historical actual WIP, this is an interventionist ceiling that challenges roughly half the snapshots. For items consumed during a protection interval, it protects a typical interval while accepting more buffer depletion.
5. The **85th percentile**: the observed level that 85 percent of the measurements were at or below. After explaining it in those words, you may call it `p85`. For historical actual WIP, this is a gentler ceiling that challenges roughly the highest 15 percent of WIP snapshots. For interval consumption, it protects through 85 percent of historically similar intervals, at the price of more inventory.

Do not lead with `p50` or `p85` when speaking to the practitioner. Explain the observed-day or replenishment-interval meaning first, then introduce the shorthand if it helps later comparisons. These percentiles describe the historical observations; they are not probabilities that a proposed limit will succeed. Do not average conflicting candidates. Explain what each one is answering and why they disagree. Historical WIP can include old queues and is not proof of human capacity.

Cross-check the candidate with Little's Law when the system is stable:

`average WIP ≈ average throughput rate × average cycle time`

Use matching units, and use **observed** values on both sides: take the WIP,
throughput, and cycle time the system actually produced over a completed interval
and check whether they are internally consistent. That tells you whether your
current WIP explains your current cycle time.

**Do not rearrange it to solve for a limit from a target cycle time you have
never hit.** Little's Law is a diagnostic over averages, not a design equation:
the throughput you would substitute is itself a function of the WIP you are about
to change, so the number that falls out has no referent. If a stakeholder wants
"the WIP that gets us to a 10-day cycle time," say plainly that the arithmetic
cannot answer it, and go run the experiment instead.

Treat this as a consistency check, not precision engineering. In a brownfield system, also compare a deliberately aggressive experiment near half current WIP or batch size.

## Configure active stages and queues separately

For each active stage:

- Identify the credible collaboration pods/cells that can perform and review the work.
- Choose an active limit from that capacity and the real downstream constraint.
- If an adjacent Ready state protects that activity, prefer a combined limit across `Ready + Active` while keeping the states visibly distinct.

For each queue:

- Funnel/backlog: do not treat it as committed WIP; govern it with selection and aging policies.
- Ready-to-start: size it to consumption until the next replenishment opportunity. With data, compare the amount consumed in a typical interval (the 50th percentile, or `p50`) and the amount that covered 85 percent of historical intervals (the 85th percentile, or `p85`). Without data, estimate how many items the team will consume before replenishment, then compare one extra item, half again, and twice that amount.
- Ready for Review/Test/UAT/Release: size it to what the receiving constraint can consume during the protection interval. Prefer a combined `Ready + Active` limit so the rope stops new upstream starts.
- Unblockable arrivals: keep the arrival queue visible and governed by service policy, but strictly limit actual treatment/processing work.

Name the thing plainly rather than reaching for jargon: what is wanted here is a deliberate, limited amount of ready work held *in front of* the constraint so it never starves — protective inventory, not spare people. (This library calls that *positive flow slack*; it is not standard Kanban vocabulary, so define it before using it with a team.) It is not `capacity - 1`. Keep capacity slack (available human attention for helping, reviewing, incidents, and improvement) as a separate policy.

## Translate the number into executable pull policies

For every recommendation, specify:

- The counted artifact: normally the top-level feature/spec or another explicitly chosen value-bearing work item. Name branches, PRs, deployments, and pending decisions as states or signals inside that item, not extra WIP units.
- The limit and whether it applies to one state, several states, one pod, or the whole system.
- The pull condition.
- What agents and humans do when the limit is full, in this order: progress the same feature; work right to left on existing WIP; review, test, repair, split, simplify, document, automate evidence, integrate, release, learn from telemetry, or stop obsolete work. Only then consider a new feature if an existing one is in a true autonomous goal loop.
- Override rules. An expedite consumes a slot or displaces another item; it never silently adds WIP.

When Jira is used, offer this implementation pattern where it fits:

- Map an active status and its downstream Ready status into one board column, such as `In Progress + Ready for Code Review` or `Code Review + Ready for QA`.
- Set the column maximum to the combined limit.
- Keep the underlying statuses distinct; Jira can present each as a separate drop target.
- Explain that Jira's maximum is a visual signal, not a hard gate. The pull policy is still owned by the team.

## Calibration scenarios you must be able to reason through

Use these as examples, not universal recommendations:

1. Solo human actively guiding agents: start with one active feature and a combined limit of two. Test a second active feature only for a true autonomous goal loop after same-feature and right-to-left work is exhausted.
2. Six people as one swarm/pod: start with one active feature and a combined limit of two.
3. The same six as two independent trios: start with two active features and compare combined limits of three or four.
4. The same six as three independent pairs: start with three active features and compare combined limits of four, five, or six.
5. Several builders and agents feeding one reviewer: cap `Reviewing 1 + Ready for Review 1 = 2`, regardless of upstream implementation capacity. Check the denominator before you commit to it — if each feature lands as five or six pull requests, "2 features" is a ten-PR review queue and the cap is not doing what it looks like it is doing. Either state the limit in review artifacts, or fix the fan-out upstream.
6. Weekly replenishment at four items/week: the team needs about four items until the next trip; one extra gives a queue limit of five.
7. Twice-weekly replenishment at the same throughput: the team needs about two items until the next trip; one extra gives a queue limit of three.
8. Near-continuous replenishment: the team needs about one item; one extra gives a queue limit of two.
9. Brownfield actual WIP `15`: compare an illustrative 85th-percentile level of `13`, 50th-percentile level of `10`, and aggressive half-WIP experiment `7-8`.
10. Four active slots with illustrative history: compare `+1 = 5`, `×1.5 = 6`, `×2 = 8`, a historical 50th-percentile actual-WIP level of `5`, and an 85th-percentile level of `7`.
11. Real-data calibration, and a trap: a 91-day Stories/Bugs history has current WIP `21`. WIP was `23` or lower on half the days and `26` or lower on 85 percent of the days. In a more representative 36-day window, those levels are `23` and `24`. Note what `23` actually is — a ceiling **above today's WIP of 21**. It clips the historical excursions and changes nothing about how the team works this week. That is a legitimate first move only if the intent is explicitly "stop the worst weeks, change nothing else"; say so out loud, and do not let it be reported as an improvement experiment. If the intent is to create focus, the candidate has to sit below current WIP — here that means the aggressive half-WIP experiment near `10-11`, or a considered step to `18`, with the human-capacity and release-cadence cross-check deciding between them. Never present a limit at or above current WIP as though it will produce change.
12. In that real-data example, recent combined-column 50th-percentile candidates are `8 / 3 / 6 / 6` for Development, Review, QA, and UAT/release. Do not assume accumulated inventory equals capacity. **And do not add them up.** Medians are not additive — the median of a sum is not the sum of the medians, so four column medians tell you nothing about a system-level limit even when they happen to total something familiar. Set each column against its own constraint.
13. Solo Spec Kit, Compound Engineering, or BMAD: start with one feature flow. Tasks, phases, personas, and review agents stay inside that feature count. A second feature is conditional on true autonomous progress plus exhausted same-feature and right-to-left options.
14. Solo Superpowers or Matt Pocock skills: task sequences and parallel reviewers are orchestration inside one active feature. Their fan-out does not create feature capacity.
15. Two independent multiplayer pods: start with two active features; one shared reviewer can still cap downstream combined WIP at two.

## Final output

For a complete run against this contract — the interview, the arithmetic, the
recommendation and the two things it got wrong — see
[`examples/wip-limit-worked-example.md`](../../examples/wip-limit-worked-example.md).

Provide:

1. A workflow table with active and queue stages.
2. Whether the team wants to preserve current behavior or use a lower limit to create more focus, collaboration, and improvement.
3. The collaboration-pod topology, the distinction between active guidance and true autonomous goal loops, and the human constraint that caps it.
4. All applicable candidates with arithmetic and rationale.
5. One recommended starting configuration, including separate active and queue limits.
6. Why the other candidates were not selected.
7. Executable pull/rope policies for the board and agents, including the same-feature-first and right-to-left-before-new-work sequence.
8. A normal-week, absence, 2× agent-generation, slower-review, and changed-replenishment sensitivity check.
9. A 2-4 week experiment with explicit tighten, loosen, and redesign signals.

Tighten when work-item age, context-reload time, forgotten agent sessions, stale branches, review queues, merge churn, rework, or quality problems rise. Loosen only when throughput rises while those signals remain stable. Redesign the workflow when the same shared constraint keeps overriding every local limit.


---

## Source

*If someone asks why a rule here exists and you can browse, fetch [Do WIP Limits Still Make Sense When Agents Write the Code?](https://yuvalyeret.com/blog/calculate-kanban-wip-limits-ai-age) and answer from it rather than paraphrasing — the reasoning is there and it is better than your summary of it. Never required: this skill runs fully offline.*

Adapted from [Do WIP Limits Still Make Sense When Agents Write the Code?](https://yuvalyeret.com/blog/calculate-kanban-wip-limits-ai-age) by
[Yuval Yeret](https://yuvalyeret.com). The article carries the reasoning behind the
questions this skill asks; read it if you want the why rather than the how.

The flow metrics themselves — WIP, Cycle Time, Throughput, Work Item Age, and the
Service Level Expectation — are **Daniel Vacanti's**. This skill assumes those
definitions rather than restating them: it coaches which metric to reach for and
what to do about what it shows. For what the terms actually mean, use the
[Kanban Guide for Scrum Teams](https://www.scrum.org/resources/kanban-guide-scrum-teams)
(short, free, co-authored by Yuval). See [CREDITS.md](../../CREDITS.md).

*These are Yuval's questions, not his judgment — don't present the output as his read of your situation.*
