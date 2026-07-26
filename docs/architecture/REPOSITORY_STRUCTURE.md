---
id: architecture.repository-structure
title: Repository Structure
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - architecture
  - repository
  - ownership
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# Repository Structure

## Purpose

This document defines the target logical organization and ownership boundaries of the framework. It does not authorize an immediate repository reorganization.

## Target structure

```text
/
├── framework/   # Shared contracts and future machine-readable specifications
├── plugins/     # Technology-specific extension packages
├── agents/      # Bounded agent role definitions
├── playbooks/   # Outcome-oriented delivery guidance
├── workflows/   # Ordered, executable procedures
├── knowledge/   # Explanatory engineering knowledge modules
├── standards/   # Mandatory requirements and controls
├── templates/   # Reusable, non-authoritative starting artifacts
├── examples/    # Illustrative applications of framework content
├── tools/       # Future framework development and validation utilities
├── docs/        # Architecture, ADRs, and contributor documentation
└── reference/   # Stable reference material and controlled vocabularies
```

## Ownership and boundaries

| Directory | Content | Boundary |
| --- | --- | --- |
| `framework/` | Neutral schemas, contracts, taxonomies, and conformance definitions | No vendor or technology-specific implementation |
| `plugins/` | Cohesive technology capability packages | Must conform to the proposed [plugin model](PLUGIN_MODEL.md); no plugin runtime exists yet |
| `agents/` | Role missions, inputs, outputs, authority, prohibitions, and evidence | Roles cannot grant approval or redefine policy |
| `playbooks/` | End-to-end guidance for a delivery outcome | Compose authoritative sources; do not copy standards |
| `workflows/` | Ordered steps, inputs, outputs, gates, and stop conditions | Must identify approvals and evidence |
| `knowledge/` | Structured explanations, trade-offs, practices, and examples | Advisory unless an authoritative source incorporates it |
| `standards/` | Mandatory requirements within a declared scope | Must have clear ownership and avoid implementation recipes |
| `templates/` | Reusable document, prompt, and configuration starting points | Examples of form, not automatically approved policy |
| `examples/` | Demonstrations and learning scenarios | Non-normative and clearly labeled |
| `tools/` | Future validators, generators, and maintenance utilities | Tool behavior must implement approved contracts |
| `docs/` | Architecture, decisions, contributor guidance, and explanatory documentation | Architecture and ADRs govern structural evolution |
| `reference/` | Controlled terms, identifiers, and stable lookup material | Changes require compatibility review |

## Where content belongs

- Put enforceable requirements in `standards/`.
- Put architectural decisions in `docs/adr/` and architecture explanations in `docs/architecture/`.
- Put durable concepts and implementation guidance in `knowledge/`.
- Put role contracts in `agents/`.
- Put outcome-level guidance in `playbooks/` and ordered procedures in `workflows/`.
- Put technology-specific bundles in `plugins/`, once that model is approved and implemented.
- Put reusable blanks or skeletons in `templates/`; put completed illustrations in `examples/`.
- Put machine-oriented core contracts in `framework/` and utilities that check them in `tools/`.
- Put controlled vocabularies and stable registries in `reference/`.

## Current repository structure

The repository currently contains root governance documents plus:

- `agents/` with an initial orchestrator definition;
- `knowledge/architecture/` with bounded-autonomy guidance;
- `playbooks/` and `workflows/` with initial feature analysis content;
- `standards/` with readiness, completion, risk, and human-oversight controls;
- `docs/architecture/` and `docs/adr/` introduced by this blueprint.

The target-only directories `framework/`, `plugins/`, `templates/`, `examples/`, `tools/`, and `reference/` do not currently exist and are not created by this sprint.

## Incremental migration

1. Add a directory only when an approved deliverable needs it.
2. Establish ownership and contracts before moving content.
3. Preserve links or update all consumers atomically.
4. Validate navigation, metadata, history, and precedence after each change.
5. Deprecate old locations before removal when external consumers may rely on them.

Major restructuring requires a dedicated ADR and explicit human approval. Convenience, symmetry, or a future-state diagram alone is not sufficient justification.

## Duplication prevention

- Every rule has one authoritative home.
- Playbooks and workflows link to standards rather than restating them.
- Examples and templates are labeled non-authoritative.
- Knowledge may explain a standard but cannot silently strengthen or weaken it.
- Plugin content references shared core guidance and contains only extension-specific material.
- When two documents conflict, apply the precedence in the [Knowledge Model](KNOWLEDGE_MODEL.md) and escalate unresolved ambiguity.
