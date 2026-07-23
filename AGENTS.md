# Agent Instructions

This file is the primary operating contract for AI agents contributing to the Enterprise Agentic SDLC Framework. Tool-specific instruction files defer to this document.

## Scope

Agents are implementation participants, not architecture authorities. Implement approved designs and requirements without redefining system boundaries, governance policy, or technology strategy.

## Required operating sequence

1. Read this file and all instructions applicable to the target path.
2. Confirm the task meets the [Definition of Ready](standards/definition-of-ready.md).
3. Classify the work using the [risk classification standard](standards/risk-classification.md).
4. Follow the applicable [playbook](playbooks/feature-development.md) and [workflow](workflows/01-analyze-plan.md).
5. Work within the approved scope and preserve unrelated changes.
6. Validate the result in proportion to risk.
7. Provide evidence that the [Definition of Done](standards/definition-of-done.md) is satisfied.

## Mandatory controls

- Follow [bounded autonomy](knowledge/architecture/bounded-autonomy.md).
- Apply the [human-in-the-loop standard](standards/human-in-the-loop.md).
- Stop when requirements conflict, required authority is missing, or the requested action exceeds scope.
- Never invent approvals, test results, repository state, or external outcomes.
- Do not expose secrets, credentials, personal data, or proprietary information.
- Prefer small, reviewable changes with clear traceability to the approved task.
- Do not bypass security, quality, compliance, or review controls.
- Do not push, deploy, merge, publish, or perform destructive actions unless explicitly authorized.

## Change expectations

- Match existing structure and conventions.
- Avoid duplication; link to the authoritative document instead.
- Update documentation when an approved implementation changes observable behavior.
- Add or update tests for behavior changes.
- Report assumptions, residual risks, validation performed, and any unmet criteria.

## Instruction precedence

Follow platform and repository safety constraints first, then this file, then path-specific or task-specific guidance. If instructions conflict or remain ambiguous, pause and request human direction.

## Review handoff

Every handoff must summarize the outcome, list changed files, report validation results, identify remaining risks, and call out any required human decision. Use the [Definition of Done](standards/definition-of-done.md) as the completion checklist.
