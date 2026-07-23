# Feature Development Playbook

## Purpose

Use this playbook to deliver an approved feature through controlled agent and human collaboration.

## Phases

1. **Analyze and plan:** Run the [analyze and plan workflow](../workflows/01-analyze-plan.md), confirm readiness, classify risk, and establish human checkpoints.
2. **Implement:** Make the smallest coherent change that satisfies approved acceptance criteria. Preserve architectural boundaries and unrelated work.
3. **Validate:** Run tests and checks proportionate to risk. Review security, privacy, compliance, accessibility, and operational effects where applicable.
4. **Review:** Present the change, evidence, assumptions, and residual risk to the required human reviewers.
5. **Deliver:** Merge, release, or deploy only with explicit authority and an appropriate rollback or recovery path.
6. **Learn:** Record material outcomes, incidents, exceptions, and reusable knowledge without duplicating authoritative standards.

## Required controls

The feature must satisfy the [Definition of Ready](../standards/definition-of-ready.md) before implementation and the [Definition of Done](../standards/definition-of-done.md) before completion. Apply [risk classification](../standards/risk-classification.md) and [human-in-the-loop](../standards/human-in-the-loop.md) throughout.

The [orchestrator agent](../agents/orchestrator.md) may coordinate these phases but cannot approve its own high-impact decisions.
