# Data Recovery Runbook

Choose `rollback` or `forward-recovery` and explain why. Bind the procedure to the schema/data migration revision and environment.

## Recovery Point

Record backup or point-in-time restore references, retention, encryption, access ownership, expected RPO/RTO, and an actual restore rehearsal in an isolated environment.

## Procedure

Define traffic stop, source-of-truth decision, restore or compensating migration, identity/sequence correction, replay boundaries, accepted-transaction handling, and post-recovery reconciliation. Destructive or lossy changes require expand/contract sequencing or a separately approved exception.

## Rehearsal Evidence

Record commands, timestamps, duration, restored schema version, reconciliation outcome, failed steps, and owners. A documented but unrehearsed procedure remains blocked for deployment approval.