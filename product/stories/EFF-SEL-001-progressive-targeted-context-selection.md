---
id: STORY-EFF-SEL-001
title: Deliver EFF-SEL-001 Progressive & Targeted Context Selection
version: 0.5.0
status: In Review
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-002
priority: Critical
---

# STORY-EFF-SEL-001 – Progressive & Targeted Context Selection

## Business Value

Provide sufficient task context with less irrelevant data, lower exposure, and attributable expansion decisions.

## Problem Statement

Whole-repository loading wastes resources and may expose unrelated sensitive material, while aggressive narrowing can omit required dependencies.

## Scope

Implement selection from product contract to standards, targets, direct dependencies, and justified broader context using the shared index and governed exclusions.

## Out of Scope

Vendor retrieval APIs, opaque ranking as sole authority, or bypass of user authorization and repository policy.

## Requirements

- Initial context MUST be bounded to the task and applicable instructions.
- Selection MUST record included and excluded assets, dependency expansion, context bytes or equivalent size, and justification.
- Sensitive context MUST require authorization and data-minimization review.
- Uncertain dependency closure MUST trigger expansion or human input.
- Local execution MUST NOT be presumed secure without data-handling evidence.

## Dependencies

[EFF-IDX-001](EFF-IDX-001-shared-repository-asset-index.md), [EFF-CTX-001](EFF-CTX-001-execution-efficiency-context-management.md), and [SPR-005-002](../sprints/SPR-005-002-repository-index-targeted-context.md).

## Required Deliverable

[Repository Index and Targeted Context](../../tools/context/README.md), including deterministic story/asset/target selection, progressive expansion, exclusions, restricted-context evidence, completeness indicators, fallback, JSON manifests, and tests.

## Acceptance Criteria

- Relevant targets and direct dependencies are selected for representative tasks.
- Broader expansion requires recorded evidence.
- Exclusions reduce irrelevant context without hiding required assets.
- Security-sensitive and ambiguous cases choose safe escalation or human input.

## Validation Requirements

Test selection accuracy, dependency closure, exclusions, authorization, ambiguity, fallback, determinism, and evidence serialization.

## Definition of Ready

The index, selection policy, sensitive-path controls, evaluation fixtures, and reviewers are available.

## Definition of Done

Selection behavior is implemented, measured, tested, documented, validated, and human-reviewed.

Implementation, automated tests, documentation, and validation evidence are complete. Human review and Product Owner approval remain pending, so this story remains **In Review**.

## Product Owner Approval

Product Owner approval is required before this story is complete.
