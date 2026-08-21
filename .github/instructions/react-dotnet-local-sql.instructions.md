---
applyTo: "target/react-dotnet-azure-sql/database/local/**,target/react-dotnet-azure-sql/backend/**/*.Tests/**"
---

# .NET local SQL Server testing rules

- Use local SQL Server only for development and automated tests; Azure SQL Database remains the compatibility target.
- Prefer Testcontainers for .NET with the pinned Microsoft SQL Server image. Start each integration suite from a clean disposable database and run the complete production migration chain.
- Use the same `Microsoft.Data.SqlClient`, mappings, T-SQL, schema names, and migration chain locally and in Azure.
- Do not use EF Core InMemory, SQLite, LocalDB, mocked repositories, relaxed constraints, or alternate dialects as database-parity evidence.
- Use runtime-assigned ports, deterministic readiness checks, sanitized synthetic fixtures, and ignored local secrets. Keep encryption enabled and restrict any local certificate exception to local/test configuration.
- Put safe start, migrate, seed, test, reset, and stop support under `target/react-dotnet-azure-sql/database/local/`; reset must verify the target is explicitly local.
- Verify readiness with a real API call that touches the database and a persisted-state assertion, not only a port or health check.
- Cache NuGet packages in CI and pin the .NET SDK, tools, packages, and SQL Server image for reproducibility.