# Human-in-the-Loop Standard

## Purpose

This standard ensures that humans retain meaningful control over consequential agent actions. It applies to all framework participants and must be used with [risk classification](risk-classification.md) and [bounded autonomy](../knowledge/architecture/bounded-autonomy.md).

## Control requirements

Human review must occur at the point where it can change an outcome, not merely after execution. The reviewer must receive the proposal, supporting evidence, known uncertainty, expected impact, and a clear approve-or-reject choice.

Explicit approval is required before an agent:

- changes architecture, governance policy, or approved scope;
- merges, deploys, publishes, releases, or changes production state;
- performs destructive or difficult-to-reverse operations;
- accesses or discloses sensitive data beyond established controls;
- accepts material security, privacy, compliance, financial, or operational risk;
- executes work classified as high or critical risk.

Approval must identify the decision, approver, scope, and time. Silence, elapsed time, prior approval for different work, or an agent's own assessment does not constitute approval.

## Escalation

Agents must pause and escalate when authority is unclear, evidence is insufficient, safeguards fail, or observed risk exceeds the approved classification. A human may narrow, reject, or reclassify the work before it resumes.

## Evidence

The delivery record must preserve requested approvals, decisions, validation evidence, exceptions, and residual risks in a system appropriate to the organization.
