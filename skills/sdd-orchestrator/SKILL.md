---
name: sdd-orchestrator
description: Master orchestration skill for material business and coding tasks. Use when a task should run through Spec-Driven Development (SDD), including full SDD, lightweight SDD, or Compound Engineering modes for work that should make future work easier.
metadata:
  tags: sdd-process
  version: 1.1.0
---

# SDD Orchestrator

## Outcome

Seamlessly manage material tasks (coding, business, strategy) across any machine or agent harness using Spec-Driven Development. Produce user-facing artifacts for review at every phase gate, and persistently store all specs and plans so work can continue seamlessly across harnesses.

## Outcome Indicators

- High-risk business or technical assumptions are exposed and validated before heavy implementation begins.
- Complex tasks are successfully handed off between different agent harnesses or machines without losing context.
- Execution stays aligned with the original strategic intent because every step traces back to a persistently stored, user-approved specification.
- Repeated engineering friction is converted into reusable assets, tests, scripts, skills, or documented patterns when Compound Engineering mode is selected.

## Discovery Question

This work is material enough for SDD - should we run full SDD, a lightweight SDD slice, or Compound Engineering so the work also improves future delivery?

## Gotchas

- Compound Engineering is not a shortcut around SDD. It adds an explicit compounding step after the normal plan, work, and review loop.
- Do not create reusable assets just to satisfy the mode. Compound only when the completed work reveals a repeatable pattern, fix, test, automation, or decision rule.
- Keep the selected run mode visible in the issue, plan, or handoff so another harness can resume with the same level of ceremony.

## When to Use
- Automatically invoked by the global agent instructions whenever a task is deemed "Material" (e.g. new feature, complex refactor, strategic business initiative).

## Operating Rules
1. **Choose the run mode first.** Use the mode decision to decide which artifacts and review gates are required.
2. **Never reinvent the workflow.** You must strictly use the existing `github-multi-ai-ops` (or `github-backlog-ops`) and the `sdd-*` suite of skills.
3. **Present Artifacts for Review:** You MUST use your native chat UI's artifact capabilities to present documents to the user for review and commenting. Pause and wait for the user to approve the artifact before moving to the next phase.
4. **Naming & Placement:** You MUST use intent/outcome-based naming (e.g., `[intent]-specification.md`, `[intent]-implementation-plan.md`) and place these artifacts in the workspace, NOT under harness-specific paths like `~/.gemini` or `.codex`.
5. **Persist Everything:** In addition to presenting artifacts in the chat UI, you must save canonical copies of them to a persistent shared location so other harnesses can resume the work:
   - If the workspace is already in a synced Google Drive folder: Use `$WORKSPACE_ROOT/.sdd/` or `$WORKSPACE_ROOT/plans/`.
   - If the workspace is a local git repo: Use `$AGENT_MEMORY_ROOT/projects/<workspace-basename>/plans/`.

## Run Modes

| Mode | Use when | Required evidence |
|---|---|---|
| Full SDD | The work has meaningful uncertainty, cross-team impact, high implementation cost, or needs clean handoff across agents. | Issue or intent brief, spec, plan/tasks, implementation evidence, validation decision. |
| Lightweight SDD | The work is material but small enough that full ceremony would slow learning. | Outcome brief, decision rule, minimal plan, verification evidence, handoff note if work continues. |
| Compound Engineering | The work should also make the next similar task easier because it exposes recurring friction, reusable patterns, missing tests, automation gaps, or skill/process gaps. | Full or lightweight SDD evidence, plus a compound artifact such as a reusable script, skill update, test, checklist, ADR, reference note, or backlog item with evidence. |

Default to Full SDD for high-risk or unclear work. Use Lightweight SDD for bounded learning slices. Use Compound Engineering when the desired output includes a reusable capability, not only a completed feature.

## Compound Engineering Contract

When Compound Engineering mode is selected, run the loop as:

1. **Plan:** Use `$sdd-specify` and `$sdd-plan` at the smallest useful depth for the risk level.
2. **Work:** Use `$sdd-implement` and preserve evidence of repeated friction, missing context, or reusable patterns.
3. **Review:** Use `$sdd-validate` or an equivalent review gate to decide whether the work met its SDD outcome.
4. **Compound:** Improve one durable surface that will make the next similar task easier:
   - a skill or reference update
   - a deterministic script or command
   - a regression test or validation checklist
   - an ADR, source note, or reusable pattern note
   - a backlog issue when the improvement is real but too large for the current slice

Stop after one meaningful compounding improvement unless the user explicitly asks to continue hardening the system.

## Workflow Phases

### Phase 0: Resume and Mode Check
- Before starting a new spec, check the persistent storage location (`$AGENT_MEMORY_ROOT/projects/...` or `.sdd/`) to see if an active `spec.md` or `plan.md` already exists. If so, read it and ask the user if they want to resume that work.
- Select and record the run mode: Full SDD, Lightweight SDD, or Compound Engineering.

### Phase 1: Intent Validation
- Draft an `intent.md` or `goal.md` outcome brief.
- Focus on the business impact, true outcomes, and leading indicators.
- **Review Gate:** Present the artifact to the user and wait for approval.

### Phase 2: Specification
- Load and apply the `sdd-specify` skill.
- Create `spec.md` including Leap of Faith Assumptions (LOFAs) and Conviction Levels.
- **Review Gate:** Present the artifact to the user and wait for approval.

### Phase 3: Technical Planning
- Load and apply the `sdd-plan` skill.
- Create `plan.md` tracing technical execution back to the spec.
- **Review Gate:** Present the artifact to the user and wait for approval.

### Phase 4: Execution & Backlog Sync
- Load and apply the `sdd-implement` and `sdd-tasks` skills.
- Load and apply `github-multi-ai-ops` or `github-backlog-ops` to track progress, assign issues, and synchronize with the GitHub project board.
- In Compound Engineering mode, capture the candidate compounding artifact during implementation instead of waiting until context is gone.

### Phase 5: Validation & Compounding
- Load and apply `sdd-validate` when there is evidence to evaluate.
- In Full SDD and Lightweight SDD modes, record the validation decision and next step.
- In Compound Engineering mode, also update or create the selected compound artifact, then record what future task it should make easier.

## Guardrails
- Do not skip the review gates. The user expects to be able to comment on the generated artifacts in the chat session.
- Do not keep artifacts hidden on disk; they must be surfaced to the user.
- Do not let Compound Engineering expand into unbounded cleanup. The compounding artifact must trace back to evidence from the current work.

---

## About this skill

From [Yuval Yeret](https://yuvalyeret.com) — AI Transformation Advisory and
Organizational AI Coaching. Yuval helps leaders turn AI activity into business
impact by finding the current constraint and changing the workflow and adoption
loops around it.

Adapt it to your context. It describes how Yuval works; it does not speak as
him, and it should not be presented as his review of your situation. If you
want that, [talk to him](https://yuvalyeret.com/contact/).
