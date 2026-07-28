# Enterprise Agentic SDLC Framework

Enterprise Agentic SDLC is an open-source framework for integrating AI agents into software delivery with bounded autonomy, explicit human oversight, and auditable engineering controls.

## Purpose

The framework helps teams apply agentic automation consistently across planning, implementation, review, and delivery. It defines shared instructions, risk controls, readiness criteria, completion criteria, and reusable workflows without prescribing a specific vendor or toolchain.

The project mission, scope, values, and capability direction are defined in the [Framework Charter](CHARTER.md).

## Framework map

| Area | Purpose |
| --- | --- |
| [Agent instructions](AGENTS.md) | Primary operating contract for implementation agents |
| [Architecture](docs/architecture/ARCHITECTURE.md) | Platform layers, component boundaries, and related architecture models |
| [Standards](standards/) | Mandatory delivery and governance controls |
| [Knowledge](knowledge/) | Architectural concepts supporting the framework |
| [Agents](agents/) | Role definitions for framework agents |
| [Playbooks](playbooks/) | Reusable end-to-end delivery guidance |
| [Workflows](workflows/) | Executable, phase-oriented procedures |

Start with the [feature development playbook](playbooks/feature-development.md) and its [analyze and plan workflow](workflows/01-analyze-plan.md).

## Architecture

The [master architecture](docs/architecture/ARCHITECTURE.md) is the entry point for the architecture document set. Supporting documents define repository organization, structured knowledge, future plugins, agent collaboration, governance, execution, security, and framework releases. Architecture decisions are recorded in [`docs/adr/`](docs/adr/).

The current repository provides the first capability layer: a knowledge and governance platform made of human-readable and AI-consumable documents. Developer tooling, validators, a CLI, plugin loading, adapters, and governed agent orchestration are planned future capabilities; they are not implemented.

## Product Management

The framework is managed as a product using versioned releases, epics, sprints, stories, decisions, and review checkpoints.

- [Release v0.4 – Enterprise Standards Framework](product/releases/REL-v0.4.md)
- [EPIC-001 – Enterprise Standards Framework](product/epics/EPIC-001-enterprise-standards-framework.md)

## Standards Foundation

The v0.4 Standards Foundation defines the contracts future enterprise standards must follow:

- [Framework Asset Taxonomy](docs/framework/FRAMEWORK_ASSETS.md)
- [Standard Metadata Schema](schemas/standard.schema.yaml)
- [Standard Authoring Template](templates/standard-template.md)
- [Standard Authoring Guide](docs/standards/STANDARD_AUTHORING_GUIDE.md)
- [Standards Catalog](standards/README.md)
- [Cross-Reference Model](docs/architecture/CROSS_REFERENCE_MODEL.md)
- [Standards Review Process](docs/governance/STANDARD_REVIEW_PROCESS.md)
- [Documentation Style Guide](docs/contributing/DOCUMENTATION_STYLE_GUIDE.md)

These foundation artifacts remain subject to Product Owner review and do not provide an automated validation engine.

## Core Engineering Standards

Sprint [SPR-004-002](product/sprints/SPR-004-002-core-engineering-standards.md) introduces eight Draft standards indexed in the [Standards Catalog](standards/README.md):

- [STD-ARCH-001 — Architecture Standard](standards/architecture/STD-ARCH-001-architecture-standard.md)
- [STD-CODE-001 — Coding Standard](standards/coding/STD-CODE-001-coding-standard.md)
- [STD-API-001 — API Design Standard](standards/api/STD-API-001-api-design-standard.md)
- [STD-TEST-001 — Testing Standard](standards/testing/STD-TEST-001-testing-standard.md)
- [STD-DOC-001 — Documentation Standard](standards/documentation/STD-DOC-001-documentation-standard.md)
- [STD-GIT-001 — Git and Branching Standard](standards/git/STD-GIT-001-git-and-branching-standard.md)
- [STD-PR-001 — Pull Request Standard](standards/pull-request/STD-PR-001-pull-request-standard.md)
- [STD-DEP-001 — Dependency Management Standard](standards/dependency-management/STD-DEP-001-dependency-management-standard.md)

These standards are not Approved until required reviews and Product Owner approval are recorded.

## Enterprise Engineering Standards

Sprint [SPR-004-003](product/sprints/SPR-004-003-enterprise-engineering-standards.md) adds seven Draft operational standards to the [Standards Catalog](standards/README.md):

- [STD-SEC-001 — Enterprise Security Standard](standards/security/STD-SEC-001-enterprise-security-standard.md)
- [STD-PERF-001 — Performance and Scalability Standard](standards/performance/STD-PERF-001-performance-scalability-standard.md)
- [STD-OBS-001 — Observability Standard](standards/observability/STD-OBS-001-observability-standard.md)
- [STD-DEPLOY-001 — Deployment Standard](standards/deployment/STD-DEPLOY-001-deployment-standard.md)
- [STD-REL-001 — Release Management Standard](standards/release/STD-REL-001-release-management-standard.md)
- [STD-INC-001 — Incident Management Standard](standards/incident/STD-INC-001-incident-management-standard.md)
- [STD-RISK-001 — Enterprise Risk Management Standard](standards/risk/STD-RISK-001-enterprise-risk-management-standard.md)

These standards define operational controls, evidence, metrics, AI boundaries, and human authority. They remain Draft until required specialist reviews and Product Owner approval are recorded.

## Core principles

- Humans retain authority over consequential decisions.
- Agents operate only within explicitly granted scope.
- Risk determines the required level of review and evidence.
- Work begins only when it meets the [Definition of Ready](standards/definition-of-ready.md).
- Work is complete only when it meets the [Definition of Done](standards/definition-of-done.md).
- Decisions, actions, and evidence must remain traceable.

## Contributing

Read [AGENTS.md](AGENTS.md) before making changes. Contribution expectations are documented in [CONTRIBUTING.md](CONTRIBUTING.md). Planned evolution is tracked in the [roadmap](ROADMAP.md), and released changes are recorded in the [changelog](CHANGELOG.md).

## License

Licensed under the [Apache License 2.0](LICENSE).
