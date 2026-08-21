# Lab 13: Run and verify the full stack

**Modernization outcome:** A browser-to-selected-backend-to-SQL workflow proven with approved
oracle cases, persisted state, accessibility, and failure behavior  
**Copilot primitives:** Integrated execution, E2E tests, runtime evidence, and cleanup

## Learn

This is the first gate that proves the components work together. It starts from a clean
database, uses the real backend and frontend contracts, drives the user-visible task,
and verifies database state. It still does not replace independent validation.

## Exercise

1. Confirm backend, database, and frontend component gates passed. Stop if any are red.
2. Give the selected Java or Dotnet Implementation Agent this control instruction:

   ```text
   Continue the approved slice for Lab 13. Verify every component gate, run the real
   local database, backend, and frontend, and execute approved browser-to-database
   cases. Record the local integrated gate and all blocked external gates. Finalize
   the implementation report and target revision, run to-validation, then stop. Do
   not claim independent parity or production readiness.
   ```

3. Require the agent to state the exact start, readiness, test, log, and cleanup
   commands from the lifecycle-bound target root README.
4. Start a clean local SQL Server, apply the authoritative migration chain, and seed
   only sanitized approved cases.
5. Start Spring Boot or ASP.NET Core with explicit local configuration. Capture stdout and stderr
   separately and verify readiness with the primary DB-touching API operation.
6. Start the React application against that backend. Verify the configured API base URL,
   CORS/CSRF behavior, and absence of browser secrets.
7. Run E2E tests through the browser for the in-scope scenarios:
   - approved success and boundary cases;
   - invalid and forbidden behavior;
   - conflict, duplicate, unavailable, retry, timeout, rollback, or restart cases that
     the slice requires;
   - keyboard flow, focus, accessible names, errors, and status announcements.
8. For every case, assert visible values/messages, HTTP outcome, database before/after
   state, ordering, versions, audit/correlation, and side effects as applicable.
9. Compare target results field by field with approved oracle outcomes. Apply only
   approved normalization to nondeterministic fields.
10. Inspect browser console, network failures, backend logs, and database results. A green
   test with unexplained server errors or protected-data logs fails the gate.
11. Stop all processes and reset only the local database. Confirm cleanup.
12. Finalize traceability, target README, runbooks, residual risks, rollback notes, and
   the implementation report. Record `activeSlice.targetRevision`.
13. Run the `to-validation` lifecycle validator.

## Gate

Do not hand off to the critic unless:

- E2E tests use the real React, selected backend, migration chain, and SQL Server;
- approved outputs and persisted state match for every required local oracle case;
- accessibility and authorization are tested through user-visible behavior;
- no unresolved critical console, network, server-log, transaction, or data mismatch
  remains;
- startup, readiness, test, reset, and cleanup commands are reproducible;
- every unavailable Azure, performance, resilience, or external-system gate is explicit;
- `to-validation` passes for the exact recorded target revision.

**Exit criterion:** The local integrated gate passes and the implementation is ready for
independent criticism, not self-certified parity or production readiness.

Continue to [Lab 14](../14-independent-validation/README.md).