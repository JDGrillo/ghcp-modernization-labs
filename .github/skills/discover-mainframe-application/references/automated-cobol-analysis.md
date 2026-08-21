# Automated COBOL structural analysis

Use repository-native analysis to accelerate discovery while preserving source authority.
The analyzer produces deterministic candidate evidence; it does not compile COBOL,
execute business behavior, establish reachability, or replace characterization.

## Run

Write the output only under the application evidence directory:

```powershell
python -B .github/skills/discover-mainframe-application/scripts/analyze_cobol.py `
  legacy-source/<source-application-path> `
  --output modernization/<application-id>/evidence/automated-analysis/analysis.json `
  --application-id <application-id> `
  --source-revision <immutable-source-revision>
```

The repository hook may deny terminal commands naming `legacy-source`. When operating
as an agent, invoke the analyzer through an approved task or test surface that has
read-only source access; never weaken the source-protection hook or copy source into a
writable directory to evade it.

## Extracted structures

- Program IDs, source hashes, and exact source coordinates.
- `COPY`, static and unresolved dynamic `CALL`, `PERFORM`, `PERFORM THRU`, `GO TO`,
  and paragraph fall-through candidates.
- Data levels, PIC metadata, signedness, scale, storage, level-88 values,
  `REDEFINES`, and `OCCURS` metadata.
- SQL operations and named table candidates.
- CICS operations and named map, mapset, transaction, program, file, queue, and
  dataset candidates.
- Basic file operations and explicit unresolved/unsupported diagnostics.

Stable analyzer IDs are derived from source revision, relative path, entity type,
qualified name, and source line. Repeated runs over the same inputs must be byte-identical.

## Reconciliation

Create `reconciliation.md` beside the analysis output. Record:

| Field | Required content |
|---|---|
| Source binding | Application ID, immutable source revision, and analyzer version |
| Coverage | Attempted, succeeded, partial, failed, warning, and error counts |
| Confirmed findings | Candidate IDs promoted into canonical artifacts with source citations |
| Rejected findings | Candidate IDs rejected and why |
| Diagnostics | Every warning/error and its resolution or gap ID |
| Missing surfaces | JCL, scheduler, BMS, CSD, DDL, runtime, or operational evidence still required |
| Reviewer | Accountable analyst; this is reconciliation, not lifecycle approval |

Use these confidence labels in canonical dependency artifacts:

- `analyzer-observed`: directly extracted syntax with an exact citation;
- `heuristic`: inferred and not proven by syntax alone;
- `analyst-confirmed`: reconciled against source or approved runtime evidence;
- `unresolved`: missing, ambiguous, unsupported, or conflicting.

Do not promote an unresolved dynamic call, approximate control-flow edge, SQL/CICS
resource name, or calculated PIC property as confirmed behavior without reconciliation.

## Stop conditions

Do not transition to planning when the declared analyzer run has failed files or error
diagnostics, is bound to a different source revision, lacks limitations, or lacks a
reconciliation record. Partial files may proceed only when every warning is reconciled
as confirmed, rejected, noncritical, or a tracked critical gap.

Never use this output as a parity oracle, production data profile, transaction model,
authorization model, restart proof, or evidence that code is reachable.