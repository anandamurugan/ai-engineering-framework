---
id: STD-INF-002
title: Standard Metadata Schema
version: 0.4.0
status: Completed
owner: Framework PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-001B
priority: Critical
---

# STD-INF-002 – Standard Metadata Schema

## Business Value

Make standard identity, ownership, status, relationships, and review requirements consistently machine-validatable.

## Scope

Define a JSON Schema expressed in YAML for standard Markdown front matter.

## Requirements

- Define required and optional metadata without forcing future relationships.
- Validate IDs, semantic versions, dates, booleans, and allowed status values.
- Include a valid example.

## Required Deliverable

[Standard Metadata Schema](../../schemas/standard.schema.yaml)

## Dependencies

- [Framework Asset Taxonomy](../../docs/framework/FRAMEWORK_ASSETS.md)
- [Sprint SPR-004-001B](../sprints/SPR-004-001B-standards-foundation.md)

## Acceptance Criteria

- The schema parses as YAML and as a JSON Schema data model.
- Required fields match the authoring template and guide.

## Validation Requirements

Parse the schema, inspect constraints, and validate representative metadata when local tooling permits.

## Definition of Ready

Metadata fields, status vocabulary, and identifier conventions are defined.

## Definition of Done

Schema consistency and syntax checks pass and the artifact is ready for Product Owner review.

## Product Owner Approval

Product Owner approval is required before this story is complete.
