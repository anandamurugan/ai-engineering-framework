# Framework Documentation Style Guide

## Purpose

This guide keeps formal framework documentation clear, concise, accessible, enterprise-oriented, and reliable for human and AI consumers. Repository-specific templates and schemas take precedence for their asset type.

## Writing style

- Lead with purpose, required outcome, and audience.
- Use short sentences, active voice, concrete nouns, and consistent terms.
- Separate requirements, recommendations, examples, and future plans.
- Explain acronyms on first use unless universally understood by the audience.
- Avoid marketing language, unsupported claims, filler, and unnecessary repetition.
- Do not use emojis in formal framework documentation unless an approved user-facing context requires them.

## Markdown heading hierarchy

- Use one H1 (`#`) matching the document title.
- Begin major sections with H2 (`##`).
- Use H3 and deeper headings only when they belong to the preceding section.
- Do not skip heading levels for visual styling.
- Keep headings concise, unique within the document, and meaningful outside surrounding prose.

## Filename conventions

- Use repository-defined stable filenames when specified by an asset convention.
- Product artifacts begin with their stable ID, for example `REL-v0.4.md` or `STD-INF-001-framework-asset-taxonomy.md`.
- Standards use `<ID>-<lowercase-kebab-title>.md`.
- General framework documents use descriptive uppercase snake case when matching existing architecture conventions, for example `CROSS_REFERENCE_MODEL.md`.
- Do not encode transient status, owner, or dates in filenames unless the asset convention requires it.

Filenames may change without changing stable asset IDs.

## Identifier usage

Use the [Framework Asset Taxonomy](../framework/FRAMEWORK_ASSETS.md). Present the stable ID in metadata and the document title. When referencing an asset, include both its ID and title when available. Never invent or reuse an identifier.

## YAML front matter

- Place front matter at the first line, bounded by `---`.
- Use two-space indentation and UTF-8 text.
- Use schema field order when a schema or template defines it.
- Quote values only when needed to preserve a scalar or represent a placeholder.
- Use YAML booleans `true` and `false`, ISO dates `YYYY-MM-DD`, and semantic versions without `v`.
- Use empty arrays rather than invented relationship targets.
- Do not store secrets, credentials, personal data, or approval signatures in front matter.

## Tables and prose

Use a table for repeated fields, comparisons, mappings, or responsibility matrices. Use prose for rationale, nuance, and sequence. Keep tables narrow enough to read, use header separators with spaces, and do not hide long normative requirements in dense cells.

## Lists

Use bullets for unordered items and numbers for meaningful sequence. Keep grammar parallel. Introduce lists with a complete sentence and a blank line. Do not create a one-item list when a sentence is clearer.

## Code blocks

- Use fenced code blocks with a language identifier when supported.
- Keep examples minimal, syntactically credible, and labeled normative or illustrative.
- Never include real credentials, sensitive values, or unsafe commands.
- Explain placeholders and expected output.
- Do not present unimplemented commands or schemas as current capabilities.

## Command examples

Commands include required working context, safe defaults, and material consequences. Prefer non-destructive and non-interactive forms. Clearly label platform-specific commands. Do not imply successful execution unless evidence exists.

## Mermaid diagrams

Use Mermaid only when relationships, sequence, hierarchy, or state are clearer visually. Provide surrounding prose so the document remains understandable without rendering. Use concise node labels, accessible direction, and syntactically reasonable diagrams. Diagrams do not replace authoritative rules or alt-context explanation.

## Relative links

- Use relative links for repository content.
- Link to the authoritative asset, not a duplicate summary.
- Include stable ID and title in labels when available.
- Verify exact filename case and heading anchors.
- Do not create active links to planned files.
- Use descriptive labels instead of “click here.”

## Terminology and capitalization

Use product names and defined framework terms consistently. Capitalize a formal asset type when referring to its defined framework meaning; use lowercase for generic concepts. Use `AI agent` rather than implying a human identity or authority.

## Normative language

- `MUST` and `MUST NOT` are mandatory.
- `SHOULD` and `SHOULD NOT` are recommended with justified exceptions.
- `MAY` is optional.

Do not use “must” casually in explanatory prose. State the subject, condition, outcome, and evidence for normative requirements.

## Accessibility

- Use descriptive headings and links.
- Do not rely on color, position, or icons alone.
- Explain diagrams and abbreviations in text.
- Keep table structure simple and code samples readable.
- Use plain language and avoid unnecessarily exclusionary terminology.
- Provide text alternatives for non-decorative images when images are introduced.

## Clear references

Avoid ambiguous pronouns such as “it,” “this,” or “they” when multiple subjects are possible. Repeat the asset or role name. Identify “the reviewer,” “the standard owner,” or “the deployment record” rather than “they” or “it.”

## Claims and current state

Distinguish:

- current implemented capabilities;
- proposed or planned capabilities;
- approved requirements;
- illustrative examples.

Do not claim that a CLI, validator, runtime, plugin, service, integration, or approval exists unless the repository or authoritative system demonstrates it.

## Examples

Examples are concise, safe, non-normative, and clearly labeled. They show the intended concept without introducing a competing requirement. Technology-specific examples must not make the shared core vendor-dependent.

## Revision history

When the asset template requires history, use:

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |

Use ISO dates and identify pending approval honestly.

## AI-generated content

AI-generated or AI-assisted content requires accountable human review before approval. The reviewer verifies sources, accuracy, applicability, normative language, relationships, sensitive-data handling, duplication, unsupported claims, and hidden vendor assumptions. An AI agent cannot approve its own output or mark human review complete.

## Preferred terminology

| Term | Preferred meaning |
| --- | --- |
| Standard | Mandatory and recommended engineering requirements within a defined scope |
| Policy | Human-approved organizational authority and constraints |
| Playbook | Outcome-oriented guidance that composes standards and workflows |
| Workflow | Ordered inputs, actions, gates, outputs, and stop conditions |
| Agent Profile | Bounded role contract for an AI agent |
| Prompt | Reviewed task instruction for a bounded agent context |
| Template | Reusable, non-authoritative artifact structure |
| Validation Rule | Deterministic conformance check with a defined result |
| Evidence | Attributable artifact supporting a claim, decision, or requirement |
| Approval Gate | Point where an authorized human decision is required before progression |
| Human Review | Accountable evaluation by an authorized person with power to change the outcome |

## Review checklist

- Purpose and audience are clear.
- Heading hierarchy, filename, ID, and metadata follow convention.
- Requirements and recommendations use correct normative language.
- Links resolve and point to authoritative assets.
- Diagrams, tables, examples, and commands are necessary and accessible.
- Terminology is consistent and claims match current state.
- Sensitive information, placeholders, ambiguity, duplication, and unsupported assertions are absent.
- AI-assisted content received accountable human review before approval.
