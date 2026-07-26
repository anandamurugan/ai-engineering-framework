---
id: adr.0002.framework-architecture
title: Adopt a Layered Framework Architecture
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - adr
  - architecture
  - platform
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# ADR-0002: Adopt a Layered Framework Architecture

## Status

Proposed. This decision has not received human approval.

## Context

The framework must serve enterprise teams, multiple AI vendors, varied engineering platforms, and different adoption stages. Without stable layers, governance can become embedded in individual tools, knowledge can be duplicated across workflows, and future runtimes can gain authority implicitly.

The current repository provides an initial knowledge and governance foundation but no CLI, validator, adapter runtime, plugin loader, or orchestration engine.

## Decision

Adopt the layered architecture defined in the [master architecture](../architecture/ARCHITECTURE.md):

- Enterprise Applications and Delivery Teams
- Agent and Tool Adapters
- Agents and Agent Collaboration
- Playbooks and Workflows
- Knowledge, Standards, and Templates
- Governance, Policy, and Human Authority as a cross-cutting control plane

Layers communicate through explicit, versioned contracts. Governance applies across every layer. Lower layers cannot grant authority to higher layers or override enterprise policy.

## Alternatives considered

### Tool-centric architecture

Organize the framework around individual AI tools and their configuration. Rejected because it couples shared policy to vendor behavior and encourages duplicated guidance.

### Workflow-only framework

Define delivery procedures without separate knowledge, governance, agent, or adapter boundaries. Rejected because authority, reusable knowledge, and integration responsibilities would remain ambiguous.

### Runtime-first platform

Build orchestration and validation software before stabilizing contracts. Rejected because automation would encode immature assumptions and imply capabilities the project has not governed.

### Flat content repository

Treat every document as equivalent guidance. Rejected because consumers cannot reliably resolve authority, applicability, or conflict.

## Consequences

### Positive

- Governance and human authority remain explicit.
- Core content stays portable across tools and vendors.
- Teams can adopt knowledge before future tooling exists.
- Components can evolve behind stable boundaries.
- Current and future capabilities can be communicated honestly.

### Negative

- More interfaces and ownership boundaries require disciplined documentation.
- Some duplication pressure moves into link and dependency management.
- Future tooling must validate cross-layer contracts and compatibility.
- Layer boundaries may require refinement as implementation evidence emerges.

## Risks

- Diagrams may be mistaken for implemented components.
- Layers may become bureaucratic silos.
- Cross-cutting governance may be applied inconsistently.
- Future adapters or plugins may leak vendor concepts into the core.

Mitigations include explicit current-state labels, incremental adoption, conformance checks, ADR review, and authoritative precedence.

## Implementation implications

- Architecture content resides in `docs/architecture/`.
- Architecture changes require ADRs and human approval.
- Knowledge, standards, roles, workflows, and future extensions keep distinct ownership.
- Developer tooling and orchestration remain future milestones.
- Repository restructuring proceeds incrementally under the [repository model](../architecture/REPOSITORY_STRUCTURE.md).
