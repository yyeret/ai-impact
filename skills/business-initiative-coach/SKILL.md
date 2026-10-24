---
name: business-initiative-coach
description: Compatibility entrypoint for the former business-initiative-coach name. Use only when an existing instruction or invocation names it; new workflows should use frame-intent for outcomes, assumptions, and leading indicators before specification.
metadata:
  tags: product-strategy, ai-transformation
  version: 2.0.0
---

# Business Initiative Coach — renamed to Frame Intent

When the sibling is installed, load and follow
[frame-intent](../frame-intent/SKILL.md), including its intent brief,
evidence-steering handoff, and coaching through the current work. It is the
canonical skill; do not run both procedures.

Mention the new name once when useful. Existing callers remain supported through
this compatibility entrypoint; use `frame-intent` in new references.

## Standalone compatibility

If only this directory was copied into a skill installation, the sibling may
not exist. Use these essentials locally; no download or web access is required:

1. Read supplied context and the receiving workflow's native artifact. Draft
   directly when possible. Otherwise ask one or two consequential questions,
   briefly explain the choice, and draft the usable parts provisionally.
2. State the desired business result and owner, whose work must change, the
   constraint, non-goals, and baseline/target/time horizon where known. Keep
   the proposed solution separate from the result.
3. Record a falsifiable causal hypothesis and critical assumptions, with IDs,
   evidence for and against, confidence, and what would disprove them.
4. Choose early indicators linked to those assumptions or outcomes. Give each
   a measure, population, baseline, proposed target or threshold, source,
   owner, review timing, and what different results would change.
5. Recommend the smallest learning step if a critical assumption lacks evidence,
   or hand off to specification if evidence supports delivery. Name the decision
   owner, timing, and trigger for reviewing adoption and outcomes.
6. Put this concise intent brief in the existing artifact or return it in chat.
   Preserve outcome/assumption/indicator links for the next agent. Separate
   confirmed, inferred, proposed, and unknown claims; invent no evidence or
   approval. Keep architecture for planning. Coach through relevant decisions
   without forcing an interview or lesson before producing usable intent.

Keep this fallback aligned with the canonical skill when maintaining the plugin.

## Source

This compatibility route points to this repository's
[Frame Intent](../frame-intent/SKILL.md), which carries the method and attribution.
