---
id: adr.0005.structured-knowledge-modules
title: Require Structured Knowledge Modules
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - adr
  - architecture
  - knowledge
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# ADR-0005: Require Structured Knowledge Modules

## Status

Proposed. This decision has not received human approval. At the time of this decision, automated validation and indexing were not implemented. REL-004 subsequently introduced the repository [validation framework](../../tools/validation/README.md); machine indexing remains unimplemented.

## Context

Free-form documentation is readable but difficult to retrieve, compare, govern, and validate consistently. AI systems need stable identity, applicability, authority, ownership, review state, and relationships; humans need clear purpose, trade-offs, examples, and decision guidance.

## Decision

Require consistent metadata and content structure for framework knowledge modules as defined in the [Knowledge Model](../architecture/KNOWLEDGE_MODEL.md).

Modules use stable identifiers, semantic versions, explicit owners, status, review state, tags, update dates, standard guidance sections, relative cross-links, validation expectations, and lifecycle information. Higher-authority governance, standards, and approved ADRs constrain knowledge.

## Alternatives considered

### Unstructured Markdown

Rejected as the target because it cannot reliably support ownership, conflict resolution, machine retrieval, or future validation.

### Fully machine-only schemas

Rejected because human readability and open contribution are primary requirements.

### Central database as the source of truth

Rejected for the current layer because it introduces technology and operational dependencies before content contracts mature.

### Tags without stable structure

Rejected because tags alone do not distinguish purpose, authority, applicability, trade-offs, or evidence.

## Consequences

### Positive

- Humans navigate modules predictably.
- AI retrieval can preserve authority and applicability.
- Ownership, status, versioning, and relationships become explicit.
- Future linting and indexing can operate on stable fields.
- Deprecation and supersession are discoverable.

### Negative

- Authors perform additional structured maintenance.
- Existing content may require incremental migration.
- Schema evolution needs compatibility discipline.
- Mechanical completeness does not guarantee guidance quality.

## Risks

- Metadata may become stale or ceremonial.
- Search systems may over-trust tags or proposed content.
- Required sections may encourage filler.
- Schema changes may break future consumers.

Mitigations include accountable ownership, review status, validation, useful “not applicable” explanations, semantic versioning, and human evaluation.

## Implementation implications

- New architecture and ADR documents use the initial metadata convention.
- Knowledge migration should be incremental and separately reviewed.
- Registered validators may check approved structures but cannot confer human approval.
- Future indexing must preserve source, version, authority, and review status.
- Conflicts use the documented precedence model and human escalation.
