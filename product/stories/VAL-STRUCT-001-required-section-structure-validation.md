---
id: STORY-VAL-STRUCT-001
title: Deliver VAL-STRUCT-001 Required-Section and Document-Structure Validation
version: 0.4.0
status: In Progress
owner: Framework PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-004
priority: High
---

# STORY-VAL-STRUCT-001 – Required-Section and Document-Structure Validation

## Business Value

Keep governed standards structurally complete, consistently ordered, and reviewable by humans and machines.

## Problem Statement

Required standard sections and ordering are defined by the template but checked manually.

## Scope

Required headings, heading order, H1 identity, mandatory-rule presence, revision-history structure, and applicable document-structure contracts.

## Out of Scope

Subjective content approval, editorial rewriting, standard-template redesign, and automatic correction.

## Requirements

- Derive required standard sections and order from the authoritative template contract.
- Report missing, duplicate, or out-of-order sections with file and heading evidence.
- Preserve human review for enforceability, evidence quality, and architectural correctness.

## Dependencies

[VAL-FWK-001](VAL-FWK-001-validation-framework-foundation.md), [Standard Authoring Template](../../templates/standard-template.md), and [Standard Authoring Guide](../../docs/standards/STANDARD_AUTHORING_GUIDE.md).

## Required Deliverable

Planned standard-structure validation rules under `tools/validation/`.

## Acceptance Criteria

- Every required standard section and its order are deterministically checked.
- Missing, duplicate, and out-of-order headings fail with actionable evidence.
- A structurally valid document is not represented as substantively approved.

## Validation Requirements

Test complete, missing-section, duplicate-section, ordering, H1, and revision-history cases.

## Definition of Ready

The authoritative template, authoring rules, result contract, and applicable file set are known.

## Definition of Done

Structure checks are deterministic, documented, evidenced, and ready for CI integration and Product Owner review.

## Product Owner Approval

Product Owner approval is required before this story is complete.
