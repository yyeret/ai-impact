---
name: prioritize-repo-issues
description: Prioritize open issues in a local GitHub repository workspace by value outcome framing and strategic goal alignment. Classifies backlog items across outcome altitude (Impact/Outcome vs Output vs Activity) and evaluates them against repository strategic goals (P0 Strategic Drivers down to P4 Distractions). Use when planning milestones or sprints, triaging an issue backlog, deciding what work to pull next, or auditing a repository queue for outcome and strategic focus.
metadata:
  tags: flow-agile, product-strategy
  version: 1.2.0
---

# Prioritize Repo Issues

## Outcome

A prioritized, strategic view of open repository issues categorized by value leverage and repo goal alignment — distinguishing core strategic value drivers from unanchored outputs, maintenance chores, and distractions — using a two-pass hybrid model (deterministic programmable triage + LLM boundary review).

## Outcome Indicators

- Open backlog items are categorized into a clear 2D priority grid:
  1. **P0: High-Leverage Strategic Value Drivers (Impact/Outcome + High Alignment)**
  2. **P1: Strategic Deliverables (Output + High Alignment — needs outcome hypothesis before pull)**
  3. **P2: Supporting Outcomes & Operational Runway (Secondary scope or critical enablers)**
  4. **P3: Routine Maintenance & Chores (Activity, defect fixes, and dependency upkeep)**
  5. **P4: Unanchored Outputs / Distractions (Low Alignment Outputs — candidates for closing or parking)**
- **Two-Pass Execution Architecture**:
  - **Pass 1 (JEV Programmable Classifier)**: Fast, deterministic triage at $0 token cost. Auto-discovers goals (local `context/repo-goals.md`, `README.md`, or remote `gh api` README), classifies altitude, applies anti-goal penalties, and partitions 80%+ of backlog items cleanly.
  - **Pass 2 (LLM Boundary Review)**: Targeted human/agent judgment on boundary edges (filtering user support Q&A out of P0, demoting package bumps to P3, and detecting semantic duplicates against published assets).
- When repo goals are unspecified, gracefully falls back to the 3-tier altitude view (Tier 1 Value Drivers, Tier 2 Deliverables, Tier 3 Maintenance).
- Prescriptive verbs ("build", "implement", "create") in feature titles are flagged as smells.
- Generic intent signals (title problem hooks, JTBD, observable deltas) are recognized across any domain (SaaS, internal platforms, content/editorial).
- Stale backlog items (untouched for ≥90 days) are surfaced for triage or closure.

## When to Run This

Run this when:
- Triaging an open GitHub issue backlog to choose what to pull next.
- Evaluating whether candidate backlog items actually advance declared repository goals.
- Auditing a repository for outcome vs output orientation.
- Preparing for a sprint or milestone planning session in a local code workspace.
- Reviewing whether recent backlog additions express observable user changes or just technical activities.

## How to Run the Tool

In any local git workspace with a GitHub remote:

```bash
# Prioritize current workspace (auto-discovers goals from context/repo-goals.md, AGENTS.md, or README.md):
python3 scripts/prioritize_issues.py

# Prioritize against explicit repo goals (file or inline text):
python3 scripts/prioritize_issues.py --goals "Deliver spec-driven agentic software factory"
python3 scripts/prioritize_issues.py --goals path/to/goals.md

# Pure 1D taxonomy scan without repo goals (classic 3-tier output):
python3 scripts/prioritize_issues.py --no-auto-goals

# Pointed at a specific remote repository (auto-fetches remote README via GitHub API):
python3 scripts/prioritize_issues.py --repo owner/repo

# Structured JSON for agentic analysis:
python3 scripts/prioritize_issues.py --json

# Custom limits and staleness thresholds:
python3 scripts/prioritize_issues.py --limit 50 --stale-days 60
```

## How to Coach Through the Results (Two-Pass Review)

When triaging the backlog with a team or agentic workflow, apply the **Two-Pass Hybrid Method**:

### Pass 1: Run JEV Programmable Triage
Execute `prioritize_issues.py` to generate the initial 2D breakdown. JEV handles the heavy lifting:
- Categorizes obvious activities (bug fixes, quarterly containers, dependency updates, maintenance spikes) into P2/P3.
- Identifies strong domain keyword matches and problem reframing hooks ("from X to Y", "can't X without Y", "?") for P0/P1.
- Auto-demotes items matching anti-goals (e.g. legacy framework debates, deprecated tooling) to P4.

### Pass 2: LLM / Human Boundary Review
Focus manual or agentic review exclusively on the boundary edges where heuristics can be tricked:

#### 1. Filter Support Q&A Out of P0
- Heuristics elevate question titles (`?`) to Outcome because strategic problem statements frequently pose questions.
- *Check:* In public repos, check whether `?` indicates a **user configuration question** or **troubleshooting request** (e.g. *"Is there a way to exclude X?"*). Demote pure support inquiries from P0 to P2 (supporting) or close as answered.

#### 2. Confirm Deliverable Altitude on P1
- Items classified as **P1** describe outputs/artifacts that align with repo goals, but are phrased prescriptively:
  - **Look for prescriptive verbs:** `build`, `create`, `implement`, `setup`, `integrate`, `develop`, `deploy`.
  - **Filter automated dependency bumps:** Confirm package upgrade requests or automated CVE notices are treated as P3 chores, not P1 strategic deliverables.
  - **Require an outcome hypothesis before pulling:**
    > `[Persona/Actor] will [do what, observably] [how much or how often], driving [repo goal/result].`

#### 3. Semantic Deduplication
- Keyword matchers cannot determine if two differently-worded issues solve the exact same problem or duplicate an already-published post/feature.
- *Check:* Review P0/P1 items against live documentation or recent releases. If an issue duplicates published work, label it `duplicate` / `hold` and move to P4.

#### 4. Review P2 & P3 (Supporting Scope & Maintenance)
- **P2:** Supporting outcomes or critical runway enablers. Pull after P0/P1 or when needed to unblock flow.
- **P3:** Routine defect repairs, dependency bumps, and chores. Keep batched and bounded; ensure chores don't crowd out P0/P1.

#### 5. Eliminate P4 (Unanchored Outputs / Distractions)
- Items classified as **P4** represent deliverables or features with low or zero alignment to the repository's declared goals:
  - Ask: *"Why is this in our active backlog? Does it serve a current milestone, or is it an unanchored idea?"*
  - Close with a polite explanation or move to an exploratory discussion rather than keeping in the active queue.

#### 6. Address Backlog Rot
- Review issues flagged with `[STALE]`.
- An issue untouched for 90+ days without progress is likely noise. Ask: *"Is this still a current priority, or can we close it?"*

---

## Source

Adapted from [Spec-Driven Agentic Harnesses and Outcome Framing](https://yuvalyeret.com/blog/spec-driven-agentic-harnesses-outcome-framing/) by [Yuval Yeret](https://yuvalyeret.com).
Implements the shared value taxonomy from `outcome-framing-coach` and repository strategic goal alignment as an offline, workspace-native CLI tool. See [CREDITS.md](../../CREDITS.md).
