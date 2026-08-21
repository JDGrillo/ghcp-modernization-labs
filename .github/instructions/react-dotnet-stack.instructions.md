---
applyTo: "target/react-dotnet-azure-sql/**"
---

# React, ASP.NET Core, and Azure SQL implementation rules

- Use the `implement-mainframe-slice` skill and require `activeSlice.backendPlatform` `dotnet-aspnet-core` with target root `target/react-dotnet-azure-sql`.
- Work only in the approved slice with named evidence, rules, interfaces, oracle cases, rollback, and acceptance gates.
- Keep React presentation, ASP.NET Core application/domain behavior, and data/integration adapters separate. The backend owns authoritative rules and transactions.
- Define and approve OpenAPI, error, identity, and database contracts before implementation. Keep them framework-neutral.
- Represent exact decimal values as JSON strings when required to avoid JavaScript precision loss; use C# `decimal` and exact Azure SQL `decimal(p,s)` internally.
- Preserve approved null/blank, date/time, ordering, concurrency, transaction, restart, failure, audit, and side-effect behavior.
- Keep every change traceable from legacy evidence through target component and actual test result.
- Maintain `target/react-dotnet-azure-sql/README.md` with executable setup, build, migration, run, test, cleanup, limitations, and security instructions. Never include secrets.
- Run focused build, static analysis, unit, component, contract, integration, accessibility, security, E2E, parity, migration, and performance gates and report actual outcomes.
- Never claim equivalence or readiness while critical mismatches, missing dependencies, unapproved assumptions, or failed gates remain.