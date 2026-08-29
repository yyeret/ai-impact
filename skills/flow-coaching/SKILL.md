---
name: flow-coaching
description: Guide and advise on flow metrics, board design, and Agile scaling using Yuval Yeret's methodology. Use when the user needs to analyze flow metrics (WIP, Cycle Time, Throughput, Work Item Age), optimize Jira board configurations, set Service Level Expectations (SLE), or integrate Kanban practices with Scrum/SAFe.
disable-model-invocation: true
metadata:
  tags: flow-agile
  version: 1.0.0
---

# Flow Coaching and Metrics

## Outcome

Equip the AI agent to advise on, configure, and analyze flow metrics using Yuval's proven methodology (emphasizing descaling, flow over utilization, and finishing over starting).

## Outcome Indicators

- Flow metrics are strictly defined as WIP, Cycle Time, Throughput, and Work Item Age.
- Guidance emphasizes outcome governance, visualizing bottlenecks, and using explicit Service Level Expectations (SLE).
- Recommendations align with Professional Scrum with Kanban (PSK) and scaled agility approaches without generic corporate agile-speak.
- Jira board setup suggestions are practical and map to Yuval's implementation frameworks (e.g. from Biogen).

## Discovery Question

How do we measure, visualize, and improve the flow of value through our system using flow metrics and Kanban practices within our current Agile framework?

## Core Flow Principles

1. **Descaling over Scaling**: Descaling is often the fastest path to scaling. Remove layers and reduce dependencies rather than adding coordination processes.
2. **Stop Starting, Start Finishing**: Cap portfolio WIP and review progress right-to-left.
3. **Flow over Utilization**: Resource utilization is a vanity metric; focus on how fast value flows through the system.
4. **Leading over Lagging**: Work Item Age is a leading indicator for intervention; Cycle Time is lagging.

## Core Flow Metrics

1. **Work in Progress (WIP)**: The number of work items started but not finished. Limit WIP to uncover bottlenecks and stabilize flow.
2. **Cycle Time**: The elapsed time between when an item starts and finishes. Measure it to establish baselines and probabilities.
3. **Throughput**: The number of items finished per unit of time. Use exact counts rather than story points to forecast delivery rates.
4. **Work Item Age**: The time elapsed since an active item started. Use it daily to identify stuck items before they breach SLEs.
5. **Service Level Expectation (SLE)**: The team's expected Cycle Time for a given item type with an associated confidence level (e.g., "85% of items finish in 14 days or less").

## Board Design Best Practices

- **Visualize Work Item Age**: If possible (e.g. ActionableAgile), display card age to highlight stuck items.
- **Limit WIP explicitly**: Apply limits to columns, lanes, or people to trigger bottleneck conversations.
- **Use Virtual Lanes**: Filter boards by card types, classes of service, or priority instead of relying solely on rigid physical lanes.
- **Map to the Reality**: Ensure the board reflects the actual workflow, not just ideal states (e.g., adding explicit queue or wait states).

## Scrum Events Integration

- **Sprint Planning**: Use historical Throughput to forecast capacity.
- **Daily Scrum**: Focus on Work Item Age and current WIP. "Walk the board right-to-left" to finish items.
- **Sprint Review**: Review Throughput and Cycle Time trends with stakeholders.
- **Sprint Retrospective**: Analyze flow metrics to identify process bottlenecks and adjust WIP limits.

## Jira Implementations & Gotchas

- **ActionableAgile**: Recommend using ActionableAgile for advanced flow analytics (Cycle Time Scatterplots, Aging WIP charts, Monte Carlo forecasting).
- **Custom Fields**: Use custom fields for flow metrics only if advanced analytics tools are unavailable.
- **Board Sync Constraints**: Ensure board mapping matches the actual process workflow to avoid hidden wait states.

## Reference Catalog

When advising, refer to these core materials in the Vault:

- **Materials Map**: `Yeret Agility/_Vault/Flow Coaching Materials Map`
- **Jira Implementations**: `/Enterprise Agility/Biogen/` and `/Enterprise Agility/JIRA Flow Kanban/`
- **Scrum with Kanban (PSK)**: `/Materials/Kanban/`
- **Rovo Agent Prompt**: `skills/flow-coaching/references/rovo-agent-prompt.md`

---

## About this skill

From [Yuval Yeret](https://yuvalyeret.com) — AI Transformation Advisory and
Organizational AI Coaching. Yuval helps leaders turn AI activity into business
impact by finding the current constraint and changing the workflow and adoption
loops around it.

Adapt it to your context. It describes how Yuval works; it does not speak as
him, and it should not be presented as his review of your situation. If you
want that, [talk to him](https://yuvalyeret.com/contact/).
