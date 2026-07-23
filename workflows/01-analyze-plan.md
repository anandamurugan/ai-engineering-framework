# Workflow 01: Analyze and Plan

## Objective

Transform an approved request into an implementation-ready plan without changing repository or external state.

## Inputs

- Approved request or issue
- Acceptance criteria
- Repository and applicable instructions
- Known architecture, constraints, and dependencies

## Procedure

1. Read [AGENTS.md](../AGENTS.md) and all path-specific instructions.
2. Inspect the relevant repository state and identify affected boundaries.
3. Restate the desired outcome, scope, exclusions, and assumptions.
4. Identify dependencies, access needs, compatibility concerns, and validation options.
5. Classify risk using the [risk classification standard](../standards/risk-classification.md).
6. Define checkpoints required by the [human-in-the-loop standard](../standards/human-in-the-loop.md).
7. Decompose implementation into ordered, testable tasks with clear owners.
8. Compare the result with the [Definition of Ready](../standards/definition-of-ready.md).
9. Resolve evidence-based gaps; escalate gaps requiring authority or material decisions.

## Output

Produce a reviewable plan containing:

- outcome and acceptance criteria;
- in-scope and out-of-scope work;
- affected components and dependencies;
- risk level and rationale;
- implementation and validation tasks;
- required human decisions;
- assumptions, open questions, and stop conditions.

Implementation may begin only after readiness criteria and required approvals are satisfied. Completion is later assessed against the [Definition of Done](../standards/definition-of-done.md).
