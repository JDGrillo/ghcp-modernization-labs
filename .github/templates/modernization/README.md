# Modernization artifact contract

Copy these JSON templates into the application-scoped paths documented in
`modernization/README.md`. JSON indexes carry lifecycle state and stable references;
Markdown artifacts carry the detailed evidence, analysis, decisions, and findings.
The validator checks that referenced JSON artifacts agree with the lifecycle manifest
on application, source, slice, plan, contract, oracle-set, backend platform, target
root, and target revisions.

## Automated discovery evidence

Automated COBOL analysis is optional. Declare it in `discovery-index.json` with
`automatedAnalysis.inScope`. When selected, store the schema-conforming JSON artifact
and its human reconciliation under
`modernization/<application-id>/evidence/automated-analysis/`. The validator requires
matching application and source revision, `candidate-evidence-only` capability, zero
failed files and error diagnostics, explicit limitations, and an existing
reconciliation path. Partial coverage and warnings remain visible and must be resolved
or tracked as gaps before review. Analyzer output is never an approval, parity oracle,
runtime reachability proof, or substitute for JCL, scheduler, BMS, CSD, Db2, file,
operational, and characterization evidence.

For an active slice, choose exactly one supported pair:

| `backendPlatform` | `targetRoot` |
|---|---|
| `java-spring` | `target/react-spring-azure-sql` |
| `dotnet-aspnet-core` | `target/react-dotnet-azure-sql` |

The choice is a reviewed planning decision. Changing it requires a new plan revision
and approval; do not implement both alternatives in one slice.

## Data migration contract

Before `to-implementation`, `slice-plan-index.json` must contain `dataMigration`. For
in-scope data, copy and complete the source-to-target map, data profile, migration
runbook, reconciliation plan, and recovery runbook templates. The validator requires
all five repository-bound paths, non-negative count/reject tolerances, an exact
control-total tolerance, a canonical hash method, and `rollback` or
`forward-recovery`. If data movement is genuinely out of scope, record the reason and
an approved decision path. Protected extracts, row-level rejects, snapshots, and
backups remain outside Git.

## Stable identifiers

Use uppercase, hyphen-separated identifiers with these prefixes:

- `APP-` application;
- `RULE-` business rule;
- `IFACE-` interface;
- `TASK-` user or batch task;
- `ORACLE-` characterization case;
- `SLICE-` implementation slice;
- `RISK-`, `GAP-`, and `DEC-` risk, gap, and decision.

Identifiers are immutable after publication. Correct descriptions or supersede an
identifier; do not silently reuse one for different behavior.

## Lifecycle transitions

Run the validator before a handoff:

```powershell
python -B .github/scripts/validate_lifecycle.py `
  modernization/<application-id>/lifecycle.json `
  --transition to-planning
```

Supported transitions are `to-planning`, `to-implementation`, `to-validation`,
`to-deployment-plan`, `to-deployment-apply`, `to-azure-validation`, and
`to-next-slice`. An agent may prepare a manifest, but only an accountable human or
external approval process may set `approval.decision` to `approved`.

Every transition from implementation onward requires `activeSlice.targetRevision`.
Deployment-plan and deployment-report artifacts bind the Terraform revision,
environment, saved-plan digest, approval, apply result, and rollback evidence to that
target. A successful apply does not by itself establish parity or readiness.
