# Lab 12: React frontend

**Modernization outcome:** An accessible React task that implements the approved UI
contract and handles all required states without duplicating backend rules  
**Copilot primitive:** Frontend path instructions plus contract and accessibility checks

## Learn

The frontend is validated first as a component against the approved API contract. A
contract stub may make component states deterministic, but only the next lab can prove
that the real browser, backend, and database agree.

## Exercise

1. Continue with the selected Java or Dotnet Implementation Agent and inspect the frontend instructions and
   React skill reference.
2. Give the agent this control instruction:

   ```text
   Continue the approved slice for Lab 12. Verify the domain, backend/API, and
   database gates, then implement only the React user task against the approved API
   contract. Run and record the frontend component, contract, keyboard, and
   accessibility gate, then stop for learner review. Do not claim full-stack proof.
   ```

3. Generate or derive TypeScript API types from the approved OpenAPI contract.
4. Implement the approved route and user task with semantic HTML and native controls.
5. Keep authoritative calculations, validation, authorization, and state transitions
   in the selected backend. Treat exact monetary JSON values as strings.
6. Implement the in-scope loading, empty, success, validation, forbidden, conflict,
   stale, unavailable, retry, timeout, partial, and unexpected states.
7. Add component tests that assert roles, labels, values, messages, actions, permissions,
   API requests, response handling, focus movement, and status/error announcements.
8. Run the package manager’s locked install, format/lint, TypeScript typecheck, unit and
   component tests, OpenAPI contract checks, and automated accessibility checks.
9. Start the development or preview server using the documented command. Open the page
   at desktop and mobile viewports; verify keyboard-only completion, focus, reflow, and
   no overlapping or clipped content.
10. Record screenshots only as supporting evidence. Do not treat snapshots as behavior
   or accessibility proof.
11. Update traceability and the draft implementation report.

## Gate

Do not continue unless:

- generated/derived API types match the approved contract with no duplicate DTO drift;
- required UI states and exact displayed values have behavioral assertions;
- keyboard, focus, labels, error summary, and async announcements are verified;
- route guards are not presented as server authorization;
- the frontend has no database access, secrets, authoritative arithmetic, or duplicated
  business state transitions;
- all frontend component checks pass and their mocked boundaries are documented.

**Exit criterion:** The frontend component gate passes; real full-stack behavior remains
explicitly unproven.

Continue to [Lab 13](../13-full-stack-runtime/README.md).