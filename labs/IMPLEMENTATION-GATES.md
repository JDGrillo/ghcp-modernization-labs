# Implementation quality gates

Use these gates in Labs 9-16. They are designed to expose incorrect agent work at the
smallest responsible layer instead of discovering it during final validation.

## Stop-the-line rule

Do not continue to the next component when a required check fails, is unavailable, or
does not exercise the behavior it claims to prove. The lifecycle-selected Java or Dotnet Implementation Agent must:

1. report the exact command, exit code, environment, and failing assertion;
2. classify the result as passed, failed, skipped, or blocked;
3. repair only the current approved slice when evidence supports a repair;
4. rerun the same focused check before broadening scope;
5. update traceability and the draft implementation report immediately.

Never weaken an approved expected result, replace a real dependency with a mock, or
change an oracle merely to turn a check green.

## Required evidence record

Every check recorded in the implementation report must include:

| Field | Required content |
|---|---|
| Check ID | Stable identifier linked from traceability |
| Layer | Domain, API, database, frontend, E2E, parity, Terraform plan/apply, Azure, or nonfunctional |
| Rule/interface/task/oracle IDs | Approved behavior exercised by the check |
| Command | Exact command that actually ran |
| Environment | Tool versions, profile, database engine/image, and relevant safe configuration |
| Result | Passed, failed, skipped, or blocked plus exit code |
| Assertion | Business value, state, error, accessibility, or side effect actually verified |
| Artifact | Test report, log, screenshot, query result, or findings path |
| Limit | What this result does not prove |

“Tests passed” without the command and behavioral assertion is not sufficient evidence.

## Gate matrix

| Gate | Minimum proof | Does not prove |
|---|---|---|
| Domain | Approved rule/oracle examples and boundaries pass in framework-independent tests | HTTP, persistence, or UI behavior |
| Backend/API | Application orchestration, authorization, validation, and error contract pass focused tests | Real SQL mappings or browser workflow |
| Database | Clean/upgrade migration, metadata, restart/replay, mapped data load, rejects, reconciliation, recovery rehearsal, real SQL transactions, and a DB-touching API check pass | Azure SQL readiness or UI behavior |
| Frontend | Typecheck, component behavior, contract handling, keyboard, and automated accessibility checks pass | Real backend/database integration |
| Local full stack | Browser-to-API-to-database oracle cases and persisted state pass against a clean local database | Azure compatibility or independent parity |
| Azure compatibility | Same migrations and required integration cases pass against Azure SQL | Production readiness by itself |
| Independent validation | Critic verifies traceability, test quality, parity, source snapshot, field-map coverage, reconciliation, rejects, recovery, security, accessibility, and applicable readiness gates | Human approval or cutover authority |
| Terraform plan | Format/validate, lint, security/policy, cost, exposure, grants, deletes, protected backup/restore, database recovery, and saved-plan digest are reviewed | That resources exist or migrated data is correct |
| Terraform apply | The approved saved-plan digest converges in the named subscription/environment | Private connectivity, parity, resilience, or readiness |
| Azure deployment | Public denial, private DNS/routes, WAF/TLS, identity/RBAC, schema migration, snapshot-bound data reconciliation, rejects, diagnostics, application flow, recovery, and drift checks pass | Business cutover authority by itself |

## Fast feedback order

For each change, run the cheapest check that can falsify it:

1. formatter, parser, compiler, or typecheck for the touched file;
2. one behavior-focused test for the changed rule or component;
3. the component suite for that layer;
4. the integrated test crossing the newly connected boundary;
5. the approved end-to-end or differential case.

Do not repeatedly run the full stack while a focused domain or component test is red.

## Human review points

Pause for learner review after every component gate. The learner should be able to
follow one approved ID through source evidence, target code, test, actual result, and
known limitation before allowing the agent to continue.

Pause again before Terraform apply. The reviewer must be able to tie the saved-plan
digest to one target revision and environment, explain every delete/replacement,
privilege, public endpoint, policy exception, cost change, recovery action, and
approval owner. For database changes, the review also binds the source snapshot,
migration revision, backup/restore rehearsal, tolerances, and recovery runbook. Verify
that the agent did not write its own approval.
