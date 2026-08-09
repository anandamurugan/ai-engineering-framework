---
id: STORY-VAL-REF-001
title: Deliver VAL-REF-001 Relative-Link and Cross-Reference Validation
version: 0.4.0
status: In Review
owner: Framework PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-004
priority: Critical
---

# STORY-VAL-REF-001 – Relative-Link and Cross-Reference Validation

## Business Value

Preserve reliable repository navigation and valid relationships among governed framework assets.

## Problem Statement

Relative links and active relationship targets are manually checked and can drift as assets evolve.

## Scope

Relative Markdown links, exact-case paths where supported, metadata relationship targets, label-to-target IDs, and prohibited broken future references.

## Out of Scope

External-site availability, speculative future relationships, automatic link rewriting, and approval of relationship meaning.

## Requirements

- Detect missing relative-link targets and invalid active standard relationships.
- Validate stable IDs against linked target metadata where the cross-reference model requires it.
- Permit legitimate conceptual relationship cycles while rejecting prohibited dependency cycles when representable.

## Dependencies

[VAL-FWK-001](VAL-FWK-001-validation-framework-foundation.md) and the [Cross-Reference Model](../../docs/architecture/CROSS_REFERENCE_MODEL.md).

## Required Deliverable

Planned relative-link and cross-reference validation rules under `tools/validation/`.

## Acceptance Criteria

- Broken repository-relative links and missing active relationship IDs fail with source and target evidence.
- Valid conceptual bidirectional relationships pass.
- Future planned text is not treated as an active dependency.

## Validation Requirements

Test valid, missing, wrong-case, anchor-bearing, planned-text, ID-mismatch, and permitted-cycle cases as supported.

## Definition of Ready

The cross-reference model, applicable Markdown set, relationship fields, and runner contract are known.

## Definition of Done

Link and relationship checks are deterministic, documented, evidenced, and ready for CI integration and Product Owner review.

## Product Owner Approval

Product Owner approval is required before this story is complete.
