# Lab 10: Selected backend and API

**Modernization outcome:** An executable backend component that enforces the approved
use case and public contract without depending on a fake database for parity claims  
**Copilot primitive:** Backend path instructions plus focused implementation checks

## Learn

This lab proves the domain-to-application-to-HTTP path. It does not claim persistence
works. API component tests may isolate infrastructure, but mocks are labeled component
evidence and cannot satisfy the database or parity gates.

**Prerequisite:** The Lab 9 domain check is recorded as passed in the draft
implementation report with its exact command, environment, assertion, result, artifact,
and limit. If it is failed, skipped, blocked, or stale after a domain change, stop and
return to Lab 9.

## Exercise

1. Continue with the Java or Dotnet Implementation Agent selected by the lifecycle.
2. Give the agent this control instruction:

   ```text
   Continue the approved slice for Lab 10. Verify the recorded domain gate, then
   implement only the selected backend application and API component. Run and record the
   backend/API gate, then stop for learner review. Do not add migrations, a real
   persistence adapter, or frontend code in this run.
   ```

3. Confirm the implementation report still binds the application, source, slice, plan,
   contract, oracle-set, backend, and target-root identities from the approved
   lifecycle state. Do not carry results from a different target or plan revision.
4. Inspect the approved OpenAPI, error, identity, and transaction contracts before code.
5. Implement application orchestration, ports, authorization, validation, idempotency,
   concurrency behavior, transaction intent, API mapping, safe errors, and correlation.
6. Require explicit DTO-to-domain mapping; do not expose persistence entities or add a
   concrete database adapter.
7. Add focused tests for:
   - successful approved oracle cases;
   - transport syntax versus authoritative business validation;
   - unauthorized and forbidden behavior;
   - invalid, conflict, stale, duplicate, and unexpected errors that apply;
   - exact response values, status codes, safe messages, and correlation identifiers;
   - no protected data or internal exception detail in responses or logs.
8. Run the backend compile/static checks, domain suite, API component tests, and OpenAPI
   contract validation using the documented wrapper commands.
9. If the backend can start without persistence by approved design, call its health
   endpoint. Label this process evidence only; a green health endpoint does not prove
   the use case or database.
10. Update traceability and the draft implementation report before continuing. Record
    every mock, stub, or in-memory adapter in the evidence limit and confirm no result
    is classified as database integration or parity.

Use the matching path guidance: Spring MVC/Security and Java mappings for
`java-spring`, or ASP.NET Core endpoints/policy authorization/Problem Details and C#
mappings for `dotnet-aspnet-core`. Both must implement the same approved OpenAPI and
error contracts.

## Gate

Do not continue unless:

- domain, application, and adapter dependencies point inward as designed;
- every use case enforces authenticated identity and policy authorization;
- API requests and responses match the approved contract exactly;
- business failures use approved public errors while unexpected causes remain diagnosable;
- focused backend checks pass with exact commands and assertions recorded;
- mocked infrastructure is clearly identified and not called integration or parity;
- no migration, concrete SQL adapter, frontend feature, or infrastructure code was
   added; those belong to later labs.

**Exit criterion:** The backend/API component gate passes; real SQL behavior remains
explicitly unproven.

Continue to [Lab 11](../11-database-integration/README.md).