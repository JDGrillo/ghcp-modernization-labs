# Lab 14: Independent validation

**Modernization outcome:** A revision-bound gate report and the narrowest supported
parity or readiness verdict  
**Copilot primitive:** Independent critic agent with evidence-only edit authority

## Learn

Validation uses a fresh role and context to seek falsifying evidence. The critic may
execute checks and write new validation artifacts, but it may not repair product code,
tests, plans, or approved expected outcomes.

## Exercise

1. Inspect the Validation Critic agent, validation skill, verification hierarchy, and
   full-stack quality gates.
2. Use the implementation handoff **Run independent validation**.
3. Confirm the critic freezes all application, source, slice, plan, contract,
   oracle-set, target, environment, and validation-run identities.
4. Require the critic to rerun applicable checks rather than accept the implementation
   report at face value.
5. Review its bidirectional traceability, test criticism, differential comparison,
   security, accessibility, database, concurrency, performance, resilience, restart,
   rollback, operations, and Azure evidence as applicable.
6. Require independent comparison of the source snapshot identity, field-map coverage,
   schema metadata, row counts, exact control totals, canonical hashes, quarantined
   rejects, tolerance exceptions, and recovery rehearsal. Schema success alone fails
   the data gate.
7. Check that generated tests, mocks, snapshots, health checks, local SQL, and E2E each
   receive only the claim their evidence supports.
8. Review findings before the summary. Unavailable evidence is blocked or skipped,
   never passed.
9. If validation fails, return findings to the lifecycle-selected implementation agent, repair only the
   affected component, rerun that component gate and all downstream gates, record a new
   target revision, and start a new independent validation run.
10. For this curriculum, continue to the enterprise Azure path. Run the lifecycle
   validator with `--transition to-deployment-plan`; the deployment handoff reruns the
   same gate before planning. `to-next-slice` is the supported alternative when a real
   program intentionally defers Azure deployment, but do not take it before Labs 15-16.

## Gate

The canonical report must identify revisions, commands, exit codes, environments,
oracle coverage, mismatches, gate states, residual risks, approvals, and rollback
status. Its verdict must be no broader than the evidence, for example:

- component checks passed;
- local integrated slice passed;
- differential parity passed for named oracle cases;
- Azure compatibility blocked;
- production readiness not assessed.

**Exit criterion:** The slice has an independently supported `passed` verdict for the
exact target revision, every repair was rechecked, and `to-deployment-plan` passes.

Continue to [Lab 15](../15-enterprise-azure-plan/README.md).