# Risk Classification Standard

## Purpose

Risk classification determines agent autonomy, validation depth, and human oversight. Classify work by its highest credible impact across security, privacy, compliance, financial loss, service availability, data integrity, reversibility, and affected users.

| Level | Typical characteristics | Minimum control |
| --- | --- | --- |
| Low | Local, reversible, limited impact; no sensitive data or production effect | Standard review and automated validation |
| Medium | Shared behavior or moderate operational impact; recovery is understood | Independent human review and targeted testing |
| High | Production, sensitive data, security boundary, broad user impact, or difficult rollback | Explicit approval before execution and before release; comprehensive evidence |
| Critical | Safety, legal, systemic, irreversible, or enterprise-wide consequences | Designated authority approval, separation of duties, staged execution, and documented recovery plan |

## Classification rules

- Use the highest applicable level; do not average risks.
- Treat uncertainty as increased risk until evidence reduces it.
- Reclassify when scope, dependencies, data, or observed behavior changes.
- Record the rationale, required controls, and approver.
- Organizational policy may impose stricter controls.

Apply approval checkpoints from the [human-in-the-loop standard](human-in-the-loop.md) and validation criteria from the [Definition of Done](definition-of-done.md).
