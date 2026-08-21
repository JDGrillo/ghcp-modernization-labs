---
applyTo: "target/react-dotnet-azure-sql/database/**,target/react-dotnet-azure-sql/backend/**/Migrations/**"
---

# .NET Azure SQL Database rules

- Generate Azure SQL Database-compatible T-SQL and preserve the approved source-to-target data map and exact `decimal(p,s)`, `datetime2`, Unicode, collation, fixed-character, null/blank, key, ordering, isolation, and locking semantics.
- Keep one authoritative migration chain. If using EF Core migrations, review generated SQL, prohibit automatic production migration on application startup, and execute migrations with a separate least-privilege Entra identity.
- Verify migration IDs/checksums and use a migration lock. Make data movement restartable through durable checkpoints or safely repeatable through idempotent operations; never remove or rewrite an applied migration.
- Separate schema migration, data transformation/load, and reconciliation results. Quarantine rejected rows in protected storage with stable exception IDs; never log protected values or silently discard rejects.
- Require expand/contract sequencing for destructive changes and rehearse the approved rollback or forward-recovery runbook against a restored database before deployment approval.
- Use `Microsoft.Data.SqlClient` with parameterized commands, encrypted connections, certificate validation, and Microsoft Entra managed identity in Azure. Do not use SQL passwords.
- Choose EF Core, Dapper, or direct ADO.NET through an ADR based on mapping complexity and SQL control. Do not use an in-memory provider as persistence evidence.
- Run the same migration chain against clean SQL Server locally and Azure SQL for compatibility evidence. Do not maintain a separate local schema.
- Verify metadata, constraints, indexes, query plans, transactions, concurrency, data reconciliation, performance, backup/recovery, and rollback.
- Reconcile the same immutable source snapshot using predeclared row-count, rejected-row, exact control-total, and canonical-hash tolerances. Stop on snapshot drift or a tolerance breach.
- Exclude SQL Server Agent, linked servers, `xp_cmdshell`, CLR, filesystem access, and cross-database transactions.