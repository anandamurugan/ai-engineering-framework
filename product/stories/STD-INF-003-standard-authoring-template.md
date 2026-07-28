---
id: STD-INF-003
title: Standard Authoring Template
version: 0.4.0
status: In Progress
owner: Framework PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-001B
priority: Critical
---

# STD-INF-003 – Standard Authoring Template

## Business Value

Give authors one consistent, reviewable structure for human-readable and AI-consumable enterprise standards.

## Scope

Provide schema-compatible front matter, required sections, and concise authoring prompts.

## Requirements

- Include every approved standard section in the required order.
- Explain normative language and preserve human approval authority.
- Avoid executable or technology-specific assumptions.

## Required Deliverable

[Standard Authoring Template](../../templates/standard-template.md)

## Dependencies

- [Standard Metadata Schema](../../schemas/standard.schema.yaml)
- [Sprint SPR-004-001B](../sprints/SPR-004-001B-standards-foundation.md)

## Acceptance Criteria

- Template metadata matches the schema.
- All required sections contain useful authoring comments.

## Validation Requirements

Compare template fields and section order against the schema and authoring guide.

## Definition of Ready

The metadata contract and required section list are known.

## Definition of Done

Template consistency and formatting checks pass and the artifact is ready for Product Owner review.

## Product Owner Approval

Product Owner approval is required before this story is complete.
