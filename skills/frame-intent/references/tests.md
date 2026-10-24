# Frame Intent — acceptance scenarios

Assess the produced brief and interaction, not repetition of the skill's wording.

## Routing

Should trigger:
- "Frame intent for this feature before our spec-driven workflow starts."
- "Turn these notes into outcomes, assumptions, and leading indicators."
- "We want an AI copilot. Help us say what result it should change."
- "Prepare the intent section in our existing requirements document."

Should route elsewhere:
- "Rewrite these epic titles as outcomes" → outcome-framing-coach.
- "Is this ready to commit funding?" → sniff-test.
- "Find duplicated bets across our portfolio" → sniff-test-portfolio.
- "Design the database schema" → the caller's planning workflow.

## Behavioral checks

1. **Enough context, experienced human.** A support director wants repeat contacts
   reduced from 24% to 15% within a quarter. Agents should answer the original
   question correctly; tagged repeat contacts are available weekly; retrieval
   quality is untested. A requirements document already has an Intent section.
   Pass: draft directly there, including assumptions, an early signal with a
   decision consequence, and a proportionate experiment. New thresholds are
   proposed. No obligatory interview, duplicate file, architecture, or tutorial.
2. **Solution-first novice.** "Deploy a copilot to everybody; success is 500
   activated seats." Pass: briefly explain why seats cannot establish the change
   in work; ask one or two consequential questions and start a provisional brief.
   No invented business result or full interview dump.
3. **No human available.** "Prepare intent overnight: AI review should make
   releases faster." Pass: preserve this as an assumption, draft usable parts,
   mark owner/baseline/threshold unknown, propose observing the review queue,
   and identify the decision that needs evidence. No fabricated approval.
4. **Indicator that does not steer.** "Revenue will rise next year; measure demos
   shipped weekly." Pass: explain the unsupported link, propose a changed-work
   signal and evidence source, and show what different observations would change.
   Do not promote invented targets or causality to confirmed facts.
5. **Enough evidence to deliver.** A repeated, validated workflow change has an
   owner, baseline, observed adoption and benefit, and next review date. Pass:
   recommend specification with residual assumptions visible; no mandatory pilot.
6. **Compatibility and portability.** Invoke the old name with Spec Kit, Kiro,
   or a custom requirements artifact. Pass: load the canonical skill once,
   preserve the native format, link outcomes/assumptions/indicators, and leave
   technical design to planning.

## Delivery checks

- Run `python3 scripts/validate_skills.py` from the repository root.
- Verify README, AGENTS, and triage route to the new name; old references are
  confined to compatibility and migration notes.
- Verify all four plugin manifests publish the same release version.
- Evaluate the first two cases in fresh agent contexts. Inspect handoff and
  coaching separately. Human behavior change needs subsequent observation.
