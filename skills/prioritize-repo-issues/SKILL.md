---
name: prioritize-repo-issues
description: Prioritize open issues in a local GitHub repository workspace by value and outcome framing. Runs the local workspace analyzer, classifies backlog items into three tiers (High-Leverage Value Drivers, Output Deliverables, and Maintenance Tasks), identifies prescriptive output smells, and guides reframing. Use when planning milestones or sprints, triaging an issue backlog, deciding what work to pull next, or auditing a repository queue for outcome orientation. For item-level rewrites of individual epics or directives, see outcome-framing-coach.
metadata:
  tags: flow-agile, product-strategy
  version: 1.0.0
---

# Prioritize Repo Issues

## Outcome

A prioritized, three-tier view of open repository issues categorized by value leverage — distinguishing real user and business value drivers from delivery artifacts and maintenance chores — with prescriptive verbs flagged and actionable reframing guidance.

## Outcome Indicators

- Open backlog items are categorized into three clear priority tiers:
  1. **Tier 1: High-Leverage Value Drivers (Impact & Outcome)**
  2. **Tier 2: Output Deliverables (Features & Artifacts)**
  3. **Tier 3: Maintenance, Bugs & Chores (Activity & Input)**
- Prescriptive verbs ("build", "implement", "create") in feature titles are flagged as smells.
- The team identifies which items need outcome hypotheses before pulling them into development.
- Stale backlog items (untouched for ≥90 days) are surfaced for triage or closure.

## When to Run This

Run this when:
- Triaging an open GitHub issue backlog to choose what to pull next.
- Auditing a repository for outcome vs output orientation.
- Preparing for a sprint or milestone planning session in a local code workspace.
- Reviewing whether recent backlog additions express observable user changes or just technical activities.

## How to Run the Tool

In any local git workspace with a GitHub remote:

```bash
# Human-readable report for current workspace:
python3 scripts/prioritize_issues.py

# Pointed at a specific remote repository:
python3 scripts/prioritize_issues.py --repo owner/repo

# Structured JSON for agentic analysis:
python3 scripts/prioritize_issues.py --json

# Custom limits and staleness thresholds:
python3 scripts/prioritize_issues.py --limit 50 --stale-days 60
```

## How to Coach Through the Results

When reading the results with a user or team:

### 1. Check Tier 1 First (Value Drivers)
Items classified as **Impact** or **Outcome** are top priority for investment:
- **Outcome:** Describes an observable change in what a user actually does (e.g., "Users complete onboarding self-service"). Verify that a falsifiable metric or baseline is defined.
- **Impact:** Describes a business metric improvement (e.g., "Reduce checkout churn by 10%"). Verify that the leading indicators and user behaviors driving this metric are identified.

### 2. Interrogate Tier 2 (Deliverables & Features)
Items classified as **Output** describe an artifact to build (e.g., "Build notification modal", "Add export endpoint").
- **Look for prescriptive verbs:** `build`, `create`, `implement`, `setup`, `integrate`, `develop`, `deploy`.
- **Ask the reframing question:** *"If we ship this tomorrow and nobody uses it, did we succeed?"*
- **Suggest an outcome reframe:** Use the `outcome-framing-coach` format:
  > `[Persona] will [do what, observably] [how much or how often], driving [business result].`

### 3. Triage Tier 3 (Maintenance & Activities)
Items classified as **Activity** or **Input** are defect fixes, dependency upgrades, refactoring, or infrastructure maintenance.
- Do not attempt to force outcome framing onto bug fixes or chores — they are legitimately activity-level.
- Check volume: If Tier 3 dominates the backlog, ask whether technical debt is choking product flow.
- Group related chores into cohesive operational blocks rather than scattering focus.

### 4. Address Backlog Rot
- Review issues flagged with `[STALE]`.
- An issue untouched for 90+ days without progress is likely noise. Ask: *"Is this still a current priority, or can we close it with an explanation?"*

---

## Source

Adapted from [Spec-Driven Agentic Harnesses and Outcome Framing](https://yuvalyeret.com/blog/spec-driven-agentic-harnesses-outcome-framing/) by [Yuval Yeret](https://yuvalyeret.com).
Implements the shared value taxonomy from `outcome-framing-coach` as an offline, workspace-native CLI tool. See [CREDITS.md](../../CREDITS.md).
