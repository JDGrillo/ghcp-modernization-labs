---
applyTo: "target/react-dotnet-azure-sql/backend/**"
---

# ASP.NET Core backend rules

- Use the current organization-supported .NET LTS SDK and supported ASP.NET Core release. Pin the SDK with `global.json`, pin dependencies, and do not use previews without an approved ADR.
- Separate API adapters, application orchestration, framework-independent C# domain rules, and infrastructure adapters.
- Keep domain projects independent of ASP.NET Core, EF Core, Azure SDKs, HTTP, and generated database types.
- Use C# `decimal` with explicit precision, scale, rounding, comparison, and overflow behavior. Never use `double` or `float` for authoritative business decimals.
- Use explicit domain types for identifiers, money/currency, business dates, timestamps, codes, and statuses.
- Map API DTOs, domain types, and persistence models explicitly. Never expose EF Core entities as public contracts.
- Validate transport syntax at boundaries and authoritative business invariants in application/domain code.
- Enforce authenticated identity and policy-based authorization in every use case. Validate issuer, audience, signature, lifetime, scopes, roles, and tenant rules from the approved identity contract.
- Define transactions in application services and preserve approved isolation, locks, ordering, commits, rollback, savepoints, restart, and external-side-effect behavior.
- Require idempotency and optimistic concurrency where retries or concurrent updates are possible.
- Choose controllers or minimal APIs, EF Core or Dapper/ADO.NET, and background processing from evidence and ADRs; do not default to unnecessary abstractions.
- Support explicit local, test, and Azure configuration without changing business behavior or SQL. Prefer Testcontainers for .NET with SQL Server for repeatable integration tests.
- Never silently substitute an in-memory provider, SQLite, or LocalDB as database-parity evidence, or fall back from Azure to a local database.
- Use Problem Details, correlation, protected-data redaction, health checks, metrics, logs, and OpenTelemetry traces.
- Add domain, API, integration, contract, concurrency, batch/restart, security, performance, and parity tests.