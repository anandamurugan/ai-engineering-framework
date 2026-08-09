---
id: STORY-VAL-META-001
title: Deliver VAL-META-001 Metadata, Schema, and Framework-ID Validation
version: 0.4.0
status: Done
owner: Framework PMO
release: REL-004
epic: EPIC-001
sprint: SPR-004-004
priority: Critical
---

# STORY-VAL-META-001 – Metadata, Schema, and Framework-ID Validation

## Business Value

Prevent invalid metadata, malformed stable identifiers, and duplicate framework identities from entering governed content.

## Problem Statement

Metadata and ID checks are manual even though standards have an authoritative schema and framework assets require stable identities.

## Scope

Frontmatter parsing, standard-schema validation, framework ID format, filename-to-ID consistency where defined, and repository-wide duplicate-ID detection.

## Out of Scope

Schema redesign, lifecycle approval, automatic metadata repair, and validation of future asset types without approved contracts.

## Requirements

- Validate standard metadata against the authoritative schema.
- Detect malformed and duplicate framework IDs across metadata-bearing artifacts.
- Produce deterministic, location-specific evidence without changing source files.

## Dependencies

[VAL-FWK-001](VAL-FWK-001-validation-framework-foundation.md), [Standard Metadata Schema](../../schemas/standard.schema.yaml), and [Framework Asset Taxonomy](../../docs/framework/FRAMEWORK_ASSETS.md).

## Required Deliverable

[Metadata, schema, and framework-ID validators](../../tools/validation/metadata.py) registered in the validation framework.

## Acceptance Criteria

- Valid repository metadata passes; missing, extra, malformed, or incorrectly typed standard fields fail.
- Duplicate IDs and defined filename-to-ID mismatches fail with both conflicting locations.
- Results never infer approval from schema compliance.

## Validation Requirements

Exercise valid, invalid, missing-field, extra-field, malformed-ID, and duplicate-ID fixtures or equivalent controlled cases.

## Definition of Ready

The schema, taxonomy, applicable asset set, error contract, and framework runner are available.

## Definition of Done

Metadata and ID checks are deterministic, documented, evidenced, and ready for CI integration and Product Owner review.

## Product Owner Approval

Product Owner approval is required before this story is complete.
