---
id: architecture.knowledge-model
title: Knowledge Model
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - architecture
  - knowledge
  - metadata
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---

# Knowledge Model

## Purpose

The knowledge model makes engineering guidance understandable to people, retrievable by machines, and governable over time. It defines a proposed content contract; automated indexing and validation are not currently implemented.

## Module structure

Each knowledge module should contain:

1. **Metadata:** Stable identity, title, version, status, owner, tags, consumption flags, review state, and update date.
2. **Purpose:** The outcome the module supports.
3. **Overview:** A concise explanation of the topic.
4. **Core concepts:** Terms and mental models needed to apply it.
5. **Rules:** Normative statements owned by the module, if any.
6. **When to use:** Applicable conditions.
7. **When not to use:** Exclusions and unsuitable contexts.
8. **Benefits:** Expected positive outcomes.
9. **Trade-offs:** Costs, limitations, and risks.
10. **Best practices:** Recommended applications.
11. **Anti-patterns:** Common unsafe or ineffective uses.
12. **Human guidance:** Decisions and review expected from people.
13. **AI implementation guidance:** Context, boundaries, evidence, and stop conditions for agents.
14. **Examples:** Clearly labeled, non-authoritative illustrations.
15. **Validation expectations:** Checks and evidence for correct application.
16. **Related standards:** Mandatory requirements that govern the topic.
17. **Related playbooks:** Delivery contexts that consume the module.
18. **Related knowledge:** Adjacent or prerequisite modules.
19. **References:** Primary or authoritative external sources.
20. **Change history or version information:** Material evolution and compatibility.

Sections may state “not applicable” when justified; omission must not conceal uncertainty or required controls.

## Metadata requirements

Architecture-defined modules use YAML front matter compatible with:

```yaml
---
id: knowledge.example
title: Example Knowledge Module
version: 0.2.0
status: proposed
owner: Framework Maintainers
tags:
  - knowledge
ai_consumable: true
human_reviewed: false
last_updated: 2026-07-23
---
```

The `id` is globally unique, stable across file moves, lowercase, and namespace-qualified. Titles may change without changing identity. Versions follow semantic versioning. Dates use ISO 8601.

## Ownership and review status

Every module has an accountable owner responsible for accuracy, conflicts, review cadence, deprecation, and security implications. Status values should distinguish at least `proposed`, `approved`, `deprecated`, and `superseded`. Only an authorized human review process may set `human_reviewed: true` or approve a module.

Consumers must not treat proposed content as enterprise policy. Organizational overlays may impose additional review states but may not misrepresent upstream status.

## Versioning and change lifecycle

- **Patch:** Editorial correction or non-material clarification.
- **Minor:** Backward-compatible guidance or structure.
- **Major:** Breaking meaning, contract, or precedence change.
- **Deprecation:** The module remains discoverable with replacement and removal guidance.
- **Supersession:** The module identifies its successor; consumers should resolve to the approved successor.

History must remain traceable through version control and, when useful, an in-document change summary.

## Cross-linking and searchability

Modules use relative links for repository content and stable identifiers for indexing. Titles, tags, purpose, applicability, relationships, and status should use consistent vocabulary. Links express semantic relationships; copied passages do not.

Future indexing may parse front matter, headings, links, and declared relationships. No machine index or search service is implemented today.

## Conflict resolution and precedence

Apply the most specific applicable content within this authority order:

```text
Human-approved governance and policy
        ↓
Mandatory engineering standards
        ↓
Approved architecture decisions
        ↓
Task-specific playbooks and workflows
        ↓
Knowledge and implementation guidance
        ↓
Prompts, examples, and templates
```

Higher authority constrains lower authority. A lower source may specialize but cannot contradict, waive, or silently override a higher source. Enterprise security and legal policy remain above repository content. Conflicts at the same level are resolved by applicability, approved status, version, and owner review; unresolved conflicts require human escalation.

## AI consumption rules

An agent should:

- retrieve only content applicable to the task, environment, and approved status;
- preserve source identity, version, precedence, and uncertainty;
- distinguish requirements from recommendations and examples;
- avoid combining incompatible modules without review;
- report missing, stale, conflicting, or unreviewed guidance;
- never elevate its own prompt above approved governance.

## Validation expectations

Current validation is manual. Future tooling may check front matter, unique identifiers, required sections, link integrity, status vocabulary, version syntax, relationship targets, and prohibited conflicts. Such tooling will require a separate approved contract and must not infer human approval.

## Related documents

- [ADR-0005: Structured Knowledge Modules](../adr/ADR-0005-structured-knowledge-modules.md)
- [Repository Structure](REPOSITORY_STRUCTURE.md)
- [Governance Model](GOVERNANCE_MODEL.md)
- [Bounded Autonomy](../../knowledge/architecture/bounded-autonomy.md)
