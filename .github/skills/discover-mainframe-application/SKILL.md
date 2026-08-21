---
name: discover-mainframe-application
description: "Recover and document an enterprise mainframe application's evidenced behavior from COBOL, copybooks, CICS, BMS, JCL, Db2, VSAM, files, and scheduler definitions. Use for source inventory, dependency analysis, business rules, data semantics, transaction behavior, characterization, and project README creation. Do not generate target code."
user-invocable: false
---

# Discover Mainframe Application

Produce an approved evidence package before target planning or implementation.

## Required procedure

1. Assign the application a stable `APP-` ID; copy the lifecycle and discovery-index templates from `.github/templates/modernization/` into the canonical application paths.
2. Define the application boundary, owners, immutable source revision, entry points, and explicit exclusions.
3. Reconcile extracted artifacts, encodings, fixed-record metadata, missing dependencies, and duplicates. Use [inventory_sources.py](./scripts/inventory_sources.py) when a deterministic local inventory is needed.
4. When COBOL structural analysis is in scope, follow [automated COBOL analysis](./references/automated-cobol-analysis.md), run [analyze_cobol.py](./scripts/analyze_cobol.py), preserve its diagnostics and limitations, and reconcile every promoted finding against source. Generated structure is candidate evidence, never an approval or runtime oracle.
5. Resolve calls, copybooks, maps, transactions, job steps, datasets, tables, files, queues, and external interfaces into a dependency model. Distinguish analyzer-observed, heuristic, analyst-confirmed, and unresolved edges.
6. Recover business rules and observable behavior with stable IDs and precise legacy citations.
7. Record data types, precision, scale, signs, padding, encoding, null/blank behavior, allowed values, sensitivity, and keys.
8. Recover authorization, commits, rollback, ordering, restart, return codes, failures, audit, and external side effects.
9. Capture sanitized independent legacy inputs and outcomes as characterization cases when access and approval permit. Do not manufacture an oracle from target code or automated analysis.
10. Review gaps and conflicting evidence. Stop only the affected behavior and state what verified evidence is needed.
11. Create or refresh the project README from approved findings. Include purpose, architecture context, capabilities, repository map, prerequisites, setup, operation, testing, status, limitations, security, and contribution guidance where evidenced and relevant.
12. Synchronize the discovery index and lifecycle manifest, set status to `ready-for-review`, and leave approval pending for an accountable human.

## Outputs

Create outputs under `modernization/<application-id>/inventory/`, `modernization/<application-id>/analysis/`, and `modernization/<application-id>/evidence/characterization/`. The canonical handoff is `modernization/<application-id>/analysis/discovery-index.json`; every listed artifact path must exist. At minimum produce:

- system context and entry-point inventory;
- dependency graph;
- business-rule catalog;
- data dictionary;
- transaction, failure, and restart model;
- interface and user-task inventory;
- characterization case index;
- unknowns and risk register.

Every conclusion must distinguish observed fact from interpretation or assumption. Never modify `legacy-source/` or create target architecture and code.

Load [z/OS extraction guidance](./references/zowe-extraction.md) for extraction and reconciliation work and [legacy analysis guidance](./references/legacy-analysis.md) for COBOL, CICS, JCL, Db2, VSAM, IMS, MQ, and fixed-record semantics.
