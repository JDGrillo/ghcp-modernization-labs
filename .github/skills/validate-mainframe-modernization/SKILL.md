---
name: validate-mainframe-modernization
description: "Independently validate a React, Azure SQL, and approved Java/Spring Boot or .NET/ASP.NET Core modernization slice against legacy evidence, including parity, security, performance, resilience, and readiness."
user-invocable: false
---

# Validate Mainframe Modernization

Seek evidence that can falsify the implementation. Do not modify the target or its expected results.

## Procedure

1. Require `modernization/<application-id>/lifecycle.json` and run the transition appropriate to the handoff: `to-validation` for an implementation or `to-azure-validation` for a deployment. Do not proceed unless it passes.
2. Freeze the manifest's application ID, source revision, active slice, plan revision, contract revision, oracle-set revision, target revision, artifact paths, environment, and validation-run ID.
3. Check bidirectional traceability: every in-scope rule and interface has legacy evidence, a target mapping, and a test; every target behavior has an approved source or decision.
4. Review tests for target-derived expectations, missing boundaries, mock-only claims, weakened assertions, nondeterminism, and absent persisted-state checks.
5. Run applicable domain, API, contract, frontend, accessibility, database integration, end-to-end, security, concurrency, performance, restart, and resilience checks.
6. Compare approved legacy inputs and outcomes with target outputs, errors, database post-state, ordering, audit, side effects, and return behavior.
7. Independently verify the source snapshot identity, complete field mapping, precision, rounding, fixed-width and encoding semantics, null versus blank, dates and time zones, isolation, locking, migration restart/repeat behavior, quarantined rejects, reconciliation tolerances, and recovery rehearsal. A successful schema migration is not a data-parity pass.
8. Separate local component evidence, local SQL evidence, full-stack evidence, differential parity, Azure SQL compatibility, Terraform convergence, Azure deployment behavior, production readiness, and cutover approval.
9. Classify each gate as passed, failed, skipped, or blocked. Never turn an unavailable environment or oracle into a pass.
10. Write `validation-gate-report.json` from the canonical template under the validation-run directory, update the lifecycle manifest to validation with the exact verdict, and leave lifecycle approval pending. Only `passed` may transition to deployment planning or the next slice.

## Report format

Lead with findings ordered by severity. For each finding include affected rule or interface, legacy evidence, target location, failing or missing test, observable risk, and required disposition. Then report:

- revisions and environment;
- exact commands and actual results;
- oracle coverage and mismatches;
- source snapshot, schema migration, data reconciliation, rejects, and recovery evidence;
- gate matrix;
- residual risks and approvals;
- the narrowest supported verdict and rollback status.

Compilation, generated tests, mocks, sample UI data, a green port check, and local SQL success are not independent parity or production-readiness evidence.

Use [general verification gates](./references/verification.md) and [full-stack verification guidance](./references/full-stack-verification.md) to select checks and constrain readiness claims.