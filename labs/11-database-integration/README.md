# Lab 11: Azure SQL design and local database integration

**Modernization outcome:** One authoritative migration chain and a running backend that
proves real persistence behavior against a clean local SQL Server  
**Copilot primitives:** Database path instructions, executable integration tests, and
environment-scoped configuration

## Learn

Compilation and mocked repositories cannot verify SQL syntax, mappings, constraints,
transactions, collation, or ordering. This lab introduces the first real infrastructure
boundary and verifies it before a frontend is added.

## Exercise

1. Confirm `to-implementation` validated the approved source-to-target map, aggregate
   data profile, migration runbook, reconciliation tolerances, and recovery runbook
   before writing DDL.
2. Continue with the selected implementation agent. Inspect its database and local SQL
   instructions plus the local SQL skill reference.
3. Give the agent this control instruction:

   ```text
   Continue the approved slice for Lab 11. Verify the domain and backend/API gates,
   then implement only the authoritative migration chain and real persistence
   adapter. Run and record the database integration gate, including a DB-touching
   API call and persisted-state assertion, then stop for learner review. Do not
   implement the React frontend in this run.
   ```

4. Implement one authoritative chain: Flyway/Liquibase for Java, or reviewed EF Core
   migrations or an approved SQL migration tool for .NET. Use named schemas, reviewed
   types, constraints, keys, defaults, indexes, and no automatic production DDL.
5. Add repository mappings and parameterized queries. Keep environment configuration
   explicit; prohibit H2, in-memory/SQLite substitutes, and silent fallback.
6. Use the Java or .NET Testcontainers SQL Server integration for repeatable tests when Docker is
   available. For an approved manual local database, use the orchestration under
   `database/local/` and safe ignored secrets.
7. From an empty disposable database, run:
   - the complete migration chain;
   - migration repeat/upgrade checks required by the slice;
   - migration checksum/lock, interruption, checkpoint restart, and idempotent replay;
   - metadata assertions for types, nullability, defaults, keys, constraints, indexes,
     schema names, and migration version;
   - repository mappings and exact decimal/date/null/blank/fixed-character/order cases;
   - transaction rollback, duplicate, idempotency, concurrency, and locking cases that
       apply to the approved behavior;
    - representative transformation/load, protected reject quarantine, zero-unowned-
       reject check, row counts, exact control totals, canonical hashes, and recovery
       rehearsal against the same source snapshot.
8. Start the backend with the explicit local profile and real database connection.
9. Call the primary API endpoint with a sanitized approved case and verify both the
   response and database post-state. Do not accept a port or health check alone.
10. Stop/reset only the explicitly local environment and record cleanup results.
11. Update traceability and the draft implementation report.

## Gate

Do not continue unless:

- clean migration and repository integration tests pass against real SQL Server;
- schema, seed data, and queries use the same approved schema qualifier;
- API-to-database behavior verifies output and persisted state for an approved case;
- rollback and transaction behavior are asserted where applicable;
- every source field is mapped or explicitly excluded, no value is silently truncated,
   coerced, defaulted, or discarded, and all reconciliation tolerances pass;
- destructive changes use expand/contract or an approved exception, and recovery has
   been rehearsed against a restored database;
- engine/image, profile, migration version, commands, results, and Azure differences
  are recorded;
- local success is labeled inner-loop evidence, not Azure SQL readiness.

When an approved Azure SQL environment is available, deploy the same migration chain
and rerun required compatibility cases here. If unavailable, record the Azure gate as
blocked; do not silently pass it.

**Exit criterion:** The database gate passes locally and Azure compatibility has an
honest passed, failed, skipped, or blocked status.

Continue to [Lab 12](../12-frontend/README.md).