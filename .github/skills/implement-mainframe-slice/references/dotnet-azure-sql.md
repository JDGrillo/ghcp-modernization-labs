# .NET, ASP.NET Core, and Azure SQL rules

Use the current organization-supported .NET LTS SDK and supported ASP.NET Core release.
Pin the SDK with `global.json`, centrally manage package versions where practical, and
commit the package lock strategy selected by the organization. Do not use previews in
an approved slice unless an ADR explicitly accepts their support risk.

## Architecture

- Keep C# domain and application projects independent of ASP.NET Core, Entity Framework
  Core, Azure SDKs, HTTP, and generated database types.
- Put HTTP, persistence, identity, messaging, and file concerns behind adapters.
- Use explicit DTO-to-domain and persistence-to-domain mappings. Never expose EF Core
  entities as the public OpenAPI contract.
- Use built-in dependency injection, configuration validation, Problem Details,
  OpenTelemetry, health checks, and policy-based authorization consistently.

## Business semantics

- Use `decimal` for business decimals with explicit database precision/scale and
  reviewed midpoint rounding. Never use `double` or `float` for authoritative values.
- Use explicit types for identifiers, currencies, business dates, timestamps, fixed
  codes, and statuses. Preserve approved null/blank and fixed-character semantics.
- Define transaction, isolation, concurrency token, idempotency, retry, rollback,
  restart, and external-side-effect boundaries in application services.

## Data and identity

- Choose EF Core, Dapper, or direct ADO.NET from the approved data-access ADR; do not
  default to an ORM when exact SQL or batch behavior is material.
- Use `Microsoft.Data.SqlClient`, encrypted connections, and Microsoft Entra token
  authentication in Azure. Never place a SQL password in configuration.
- Keep one authoritative Azure SQL-compatible migration chain. If EF Core migrations
  are selected, review generated SQL and make production migration execution an
  explicit, least-privilege deployment step rather than application startup behavior.

## Verification

- Use xUnit, NUnit, or MSTest according to the approved engineering standard; use real
  SQL Server integration tests and the same migration chain used for Azure SQL.
- Verify API contracts, Problem Details, authorization policies, persistence,
  transactions, concurrency, batch/restart behavior, telemetry, and approved oracle
  cases. Compilation or an in-memory provider is not database-parity evidence.