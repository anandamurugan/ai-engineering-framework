---
id: STD-TEST-001
title: Testing Standard
version: 0.4.0
status: Draft
category: Testing
owner: Framework PMO
review_cycle: P12M
mandatory: true
ai_consumable: true
human_review_required: true
effective_date: null
last_reviewed: null
supersedes: []
related_standards:
  - STD-CODE-001
  - STD-API-001
  - STD-PR-001
related_playbooks: []
tags:
  - testing
  - quality
---

# STD-TEST-001 – Testing Standard

## Purpose

Produce proportionate, reproducible evidence that software satisfies requirements and manages quality risk.
## Scope

Applies to changed behavior, integrations, contracts, security, performance, resilience, regression, data, and delivery checks.
## Definitions

- **Test level:** Scope of exercised components, such as unit, integration, contract, or end-to-end.
- **Flaky test:** Test with inconsistent results when relevant inputs are unchanged.
## Principles

Testing is risk-based, layered, deterministic, traceable, automated where valuable, and independently reviewable.
## Applicability

Every production-bound change MUST have a documented test impact and evidence proportionate to risk.
## Mandatory Rules

1. **Risk strategy.** Teams MUST map requirements, failure impact, and quality attributes to planned test levels and measurable acceptance thresholds. Evidence: test strategy and traceability.
2. **Distribution.** Teams MUST use an efficient distribution of unit, integration, contract, and end-to-end tests appropriate to architecture; omitted levels MUST be justified. Evidence: test inventory.
3. **Quality risks.** Applicable security, performance, resilience, recovery, compatibility, and regression behavior MUST be tested before release. Evidence: results and accepted gaps.
4. **Data.** Test data MUST be authorized, minimized, isolated, reproducible, and free of uncontrolled production-sensitive data. Evidence: data source and handling record.
5. **Independence.** Tests MUST control relevant time, randomness, environment, and external dependencies or document controlled integration assumptions. Evidence: reproducible execution.
6. **Flakiness.** Flaky tests MUST be quarantined only with an owner, issue, impact assessment, expiry, and compensating gate; they MUST NOT be silently retried until green. Evidence: quarantine record.
7. **Coverage.** Teams MUST define and justify measurable coverage and quality thresholds based on risk; no percentage alone proves adequacy. Evidence: threshold rationale and report.
8. **Traceability.** Failures, defects, fixes, and regression tests MUST trace to the affected requirement or risk. Evidence: linked records.
9. **CI execution.** Required tests MUST run in the approved continuous integration or equivalent controlled process and block progression according to risk policy. Evidence: immutable run result.
10. **AI tests.** AI-generated tests MUST receive human review for oracle correctness, missing cases, false confidence, data safety, and independence. Evidence: disclosure and review.
## Recommended Practices

- Teams SHOULD keep fast deterministic checks early and reserve broader tests for risks that require them.
- Teams SHOULD test observable behavior rather than implementation details.
## Prohibited Practices or Anti-Patterns

- Teams MUST NOT delete or weaken tests merely to pass a gate, fabricate results, use uncontrolled sensitive data, or treat coverage percentage as sufficient evidence.
## AI Implementation Guidance

Agents MAY propose cases and tests but MUST derive expected results from approved requirements, run available checks, disclose limitations, and stop when the correct oracle or data authorization is unclear.
## Human Review Guidance

Product and domain owners confirm expected behavior; QA confirms strategy and evidence; security and operations review applicable risks. Humans accept residual untested risk.
## Required Evidence

- Risk-based strategy, requirement mapping, test inventory, thresholds, environments, data controls
- Commands or pipeline runs, results, failures, defects, coverage, quarantines, and accepted gaps
## Validation Rules

- Automated checks SHOULD enforce required suites, failure gates, result publication, and quarantine expiry.
- Human review MUST assess risk coverage, oracle quality, gaps, data safety, and reproducibility.
## Exceptions

Follow the [Standards Review Process](../../docs/governance/STANDARD_REVIEW_PROCESS.md); record scope, risk, compensating evidence, approval, expiry, and remediation.
## Related Standards

- [STD-CODE-001 — Coding Standard](../coding/STD-CODE-001-coding-standard.md)
- [STD-API-001 — API Design Standard](../api/STD-API-001-api-design-standard.md)
- [STD-PR-001 — Pull Request Standard](../pull-request/STD-PR-001-pull-request-standard.md)
## Related Playbooks

None. Future testing playbook relationships remain planned.
## References

- [Definition of Done](../definition-of-done.md)
- [Execution Model](../../docs/architecture/EXECUTION_MODEL.md)
## Revision History

| Version | Date | Change | Author | Approval |
| --- | --- | --- | --- | --- |
| 0.4.0 | 2026-07-27 | Initial draft | Framework PMO | Pending Product Owner approval |
