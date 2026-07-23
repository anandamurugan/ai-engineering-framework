# Enterprise Agentic SDLC Framework

Enterprise Agentic SDLC is an open-source framework for integrating AI agents into software delivery with bounded autonomy, explicit human oversight, and auditable engineering controls.

## Purpose

The framework helps teams apply agentic automation consistently across planning, implementation, review, and delivery. It defines shared instructions, risk controls, readiness criteria, completion criteria, and reusable workflows without prescribing a specific vendor or toolchain.

## Framework map

| Area | Purpose |
| --- | --- |
| [Agent instructions](AGENTS.md) | Primary operating contract for implementation agents |
| [Standards](standards/) | Mandatory delivery and governance controls |
| [Knowledge](knowledge/) | Architectural concepts supporting the framework |
| [Agents](agents/) | Role definitions for framework agents |
| [Playbooks](playbooks/) | Reusable end-to-end delivery guidance |
| [Workflows](workflows/) | Executable, phase-oriented procedures |

Start with the [feature development playbook](playbooks/feature-development.md) and its [analyze and plan workflow](workflows/01-analyze-plan.md).

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
