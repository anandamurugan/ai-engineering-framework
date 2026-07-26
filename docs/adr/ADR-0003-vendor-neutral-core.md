---
id: adr.0003.vendor-neutral-core
title: Keep the Framework Core Vendor-Neutral
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - adr
  - architecture
  - vendor-neutrality
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# ADR-0003: Keep the Framework Core Vendor-Neutral

## Status

Proposed. This decision has not received human approval.

## Context

Enterprise adopters use different AI providers, developer tools, repositories, delivery platforms, and security controls. Embedding one vendor's prompts, APIs, identity model, or execution behavior in shared governance would reduce portability and make policy quality depend on product churn.

Tool-specific instruction files are still useful for translating shared expectations into a tool's supported format.

## Decision

Keep shared governance, standards, knowledge, architecture, agent roles, playbooks, and workflows independent of individual AI vendors.

Implement tool-specific behavior only through bounded adapters, tool instruction files such as `CLAUDE.md` or `.github/copilot-instructions.md`, or future plugins where technology-specific knowledge is intentional. These extensions must reference the authoritative core, declare limitations, and cannot weaken governance or human approval.

## Alternatives considered

### Optimize the core for a primary vendor

Rejected because it creates lock-in, complicates multi-vendor adoption, and lets provider capabilities shape enterprise authority.

### Maintain separate frameworks per tool

Rejected because policies and knowledge would diverge and require duplicate review.

### Use only generic prose with no adapters

Rejected because tools need precise integration guidance and capability translation; neutrality should not prevent usable extensions.

## Consequences

### Positive

- Organizations can change or combine vendors with limited core impact.
- Governance and knowledge retain stable meaning.
- Tool differences are visible at explicit boundaries.
- Shared content receives one authoritative review.

### Negative

- The core cannot rely on convenient proprietary features.
- Adapters require maintenance and compatibility testing.
- Some concepts need neutral abstractions before implementation.
- Vendor-specific optimizations may be available only in extensions.

## Risks

- Lowest-common-denominator design may limit value.
- Vendor terminology may enter the core unintentionally.
- Adapter behavior may diverge from shared contracts.
- Tool instruction files may duplicate or contradict `AGENTS.md`.

Mitigations include contract tests when tooling exists, minimal instruction shims, ownership review, and precedence validation.

## Implementation implications

- Core documents use capability-oriented language.
- Tool files defer to [AGENTS.md](../../AGENTS.md).
- Future adapters declare permissions, evidence, and compatibility.
- Technology examples remain illustrative unless packaged in an approved extension.
- Vendor-specific architecture requires separate scope and review.
