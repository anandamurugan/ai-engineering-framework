---
id: STORY-EFF-BUD-001
title: Deliver EFF-BUD-001 Context Budgets, Checkpoints & Loop Controls
version: 0.5.0
status: In Review
owner: Framework PMO
release: REL-005
epic: EPIC-002
sprint: SPR-005-003
priority: Critical
---

# STORY-EFF-BUD-001 – Context Budgets, Checkpoints & Loop Controls

## Business Value

Bound resource use and autonomous repetition while making long-running work resumable and reviewable.

## Problem Statement

Executions can expand context, retry equivalent failures, oscillate between changes, or outgrow conversational history without controlled response.

## Scope

Implement configurable multidimensional budgets, durable structured checkpoints, repeated-failure detection, and stop, reassess, escalate, or request-human-input behavior.

## Out of Scope

Universal numeric limits, checkpoints as approvals, hidden automatic budget increases, or vendor session formats.

## Requirements

- Profiles MAY bound initial files, context size, expansion, retries, repeated failures, duration, and tool invocations.
- Budget exhaustion MUST produce evidence and a governed response rather than silent continuation.
- Checkpoints SHOULD capture objective, state, files changed, decisions, unresolved questions, validation, findings, next action, and retry or escalation state.
- Identical command, patch, dependency, or test failures; oscillating changes; and context expansion without progress MUST trigger bounded loop response.
- Checkpoints MUST minimize sensitive data and MUST NOT become approvals by implication.

## Dependencies

[EFF-CTX-001](EFF-CTX-001-execution-efficiency-context-management.md), [EFF-MET-001](EFF-MET-001-efficiency-measurement-evidence-contract.md), and [SPR-005-003](../sprints/SPR-005-003-budgets-checkpoints-routing.md).

## Required Deliverable

[Execution Budgets, Checkpoints, and Routing](../../tools/execution/README.md), including configurable budget evaluation, explicit execution state, provenance-aware checkpoint persistence and resume checks, deterministic loop signatures and responses, evidence, tests, and operational commands.

## Acceptance Criteria

- Each supported budget dimension is configurable without a universal default being normative.
- Equivalent failures are detected within a defined bound and cannot retry indefinitely.
- A checkpoint resumes representative work without replaying full conversation history.
- Approval and risk authority remain external to checkpoint and automation status.

## Validation Requirements

Test boundary conditions, repeated and oscillating failures, serialization, resume accuracy, sensitive-data handling, escalation, termination, and human-input paths.

## Definition of Ready

Budget dimensions, profile ownership, checkpoint schema, loop equivalence, retention, and escalation consumers are agreed.

## Definition of Done

The implementation and failure paths are tested, documented, validated, measured, and approved by required humans.

Implementation, automated tests, documentation, and validation evidence are complete. Human review and Product Owner approval remain pending, so this story remains **In Review**.

## Product Owner Approval

Product Owner approval is required before this story is complete.
