# Data Migration Runbook

## Identity And Scope

Bind the source snapshot, source-to-target map revision, migration code revision, target environment, migration identity, and approval reference. State inclusions, exclusions, classification, retention, and authorized operators.

## Preconditions

Require verified backup/restore evidence, capacity, schema version, empty or expected target state, migration lock, source freeze or coexistence checkpoint, and least-privilege connectivity. Abort on an unexpected source/target count, schema checksum, classification, or environment.

## Execution

Define ordered extract, stage, validate, transform, load, and constraint-enable steps. State transaction boundaries, checkpoints, restart keys, idempotency, parent/child order, duplicate behavior, reject quarantine, audit fields, and timeout/retry limits. Never log protected row values.

## Stop Conditions

Stop on unmapped columns, truncation, overflow, encoding loss, unexpected null/default coercion, duplicate or orphan growth, tolerance breach, unowned rejects, checksum drift, or failed checkpoint/restart.

## Completion

Do not release the source freeze or authorize cutover until reconciliation and recovery gates have accountable sign-off.