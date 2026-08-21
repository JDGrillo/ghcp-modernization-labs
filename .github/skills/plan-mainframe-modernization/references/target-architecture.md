# Three-tier target architecture

## Contents

1. Supported platform choices
2. Tier responsibilities
3. Deployment boundaries
4. Framework mappings
5. Cross-cutting requirements
6. Architecture gate

## Supported platform choices

The presentation and database targets are fixed; planning selects one backend per slice:

- React with TypeScript for presentation.
- Java with a current organization-supported LTS JDK, supported Spring Boot release,
  and plain Java domain rules; or
- .NET with a current organization-supported LTS SDK, supported ASP.NET Core release,
  and framework-independent C# domain rules.
- Azure SQL Database for converted relational persistence.

Use organization-approved runtime versions and pin dependencies. Architecture ADRs
select the backend and decide slice-specific module, persistence, transaction,
integration, security, deployment, and coexistence details. Do not use preview releases
merely to satisfy “latest,” and do not implement both backends in one slice.
Generated relational schemas must comply with [azure-sql.md](azure-sql.md).

## Tier responsibilities

### Presentation/API tier

- REST/UI/message/file adapters, authentication context, authorization enforcement, boundary validation, protocol mapping, versioning, rate controls, and error contracts.
- No business calculations, database access, or vendor-specific records in controllers/endpoints.
- Contract-first OpenAPI, event, and file schemas where applicable.

### Application/business tier

- Use-case orchestration, domain rules, state transitions, policies, idempotency decisions, transaction demarcation, and ports for external dependencies.
- Domain types express money, dates, codes, identifiers, quantities, and states precisely.
- No HTTP, UI, ORM, queue-client, or filesystem dependencies in domain rules.

### Data/integration tier

- Repositories, Db2 coexistence and Azure SQL access, VSAM/IMS coexistence adapters, MQ/event clients, file codecs, external-service clients, caching, and technical retries.
- Map legacy record layouts and vendor types to domain types at the boundary.
- Apply timeouts, retry limits, circuit behavior, pool sizing, and telemetry without changing business outcomes.

Dependencies point from outer tiers toward application/domain abstractions. Cross-tier calls must use explicit contracts.

## Deployment boundaries

Three-tier does not require microservices. Prefer a modular monolith when:

- Business capabilities share transactions and data.
- The team or operational platform benefits from one deployable.
- Independent scaling and release cadence are not proven needs.

Split services only with evidence of a bounded context, independent ownership/deployment, an explicit data owner, and a designed consistency model. Never create one service per COBOL program or database table.

## Framework mappings

### Spring Boot

- Spring MVC/WebFlux only as justified; avoid reactive complexity for blocking dependencies.
- Plain Java domain model and application services.
- Spring Data JDBC, JPA, jOOQ, or JDBC chosen by SQL/control needs.
- Spring Batch for jobs whose restart/checkpoint semantics fit.
- Spring Security, validation, Actuator, and enterprise OpenTelemetry integration.

### ASP.NET Core

- Controllers or minimal APIs chosen for contract clarity, not novelty.
- Framework-independent C# domain model and application services.
- EF Core, Dapper, or ADO.NET chosen by mapping and SQL-control needs.
- Hosted services or an approved scheduler only when restart, checkpoint, retry, and
	operational semantics match the recovered batch behavior.
- Policy authorization, validation, Problem Details, health checks, and enterprise
	OpenTelemetry integration.

## Cross-cutting requirements

Define:

- Identity propagation, least privilege, service identities, secrets, certificate rotation, and audit.
- Input validation, output encoding, parameterized queries, dependency governance, threat model, and supply-chain controls.
- Structured logs, metrics, distributed traces, business reconciliation metrics, correlation IDs, and data redaction.
- Timeouts, retries, idempotency, circuit behavior, bulkheads, graceful shutdown, health/readiness, and capacity limits.
- Schema evolution, backward compatibility, data migration, retention, backup/restore, and disaster recovery.
- Azure SQL service tier, compatibility level, zone redundancy where required, connection limits, transient-fault policy, Microsoft Entra authentication, encryption, auditing, threat detection, and performance monitoring.
- Accessibility, localization, date/time zone rules, privacy, legal hold, and records management.
- Build reproducibility, signed artifacts, SBOM, scanning, deployment promotion, feature controls, and rollback.

## Architecture gate

Approve before broad implementation:

- System context and bounded contexts.
- Tier/module/deployment diagram and dependency rules.
- Persistence, transaction, integration, batch, identity, observability, and hosting ADRs.
- API/event/file contracts and compatibility policy.
- Data ownership, consistency, migration, and reconciliation plan.
- Azure SQL schema, source-to-target mapping, migration chain, indexing/query-plan evidence, and rollback or forward-recovery plan.
- Threat model and nonfunctional acceptance criteria.
- Incremental coexistence, cutover, and rollback approach.
- Traceability from architecture components to legacy entry points and rules.
- Approved `backendPlatform`/`targetRoot` pair and framework-selection ADR.
