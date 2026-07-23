# Bounded Autonomy

Bounded autonomy allows an agent to act independently inside explicit limits while preserving human authority over consequential decisions.

## The autonomy boundary

Every delegated task should define:

- **Objective:** the outcome the agent may pursue.
- **Scope:** the systems, files, data, and people included.
- **Permissions:** the actions and tools the agent may use.
- **Constraints:** architecture, policy, time, cost, and quality limits.
- **Checkpoints:** decisions requiring human review or approval.
- **Evidence:** the observations and validation required for handoff.
- **Stop conditions:** ambiguity, elevated risk, failed safeguards, or exhausted authority.

Within this boundary, an agent may make reversible implementation decisions that are necessary to achieve the approved objective. It may not widen its objective, grant itself authority, or treat technical capability as permission.

## Feedback and control

Effective autonomy is a closed loop:

1. Observe the current state.
2. Compare it with the approved objective and constraints.
3. Take an allowed action.
4. Validate the effect.
5. Continue, correct, or escalate.

The boundary should narrow as impact and irreversibility increase. The applicable controls are defined by [risk classification](../../standards/risk-classification.md) and the [human-in-the-loop standard](../../standards/human-in-the-loop.md).
