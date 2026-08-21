---
applyTo: "modernization/**"
---

# Modernization evidence rules

- Treat legacy citations and approved characterization outcomes as evidence, not prose to optimize or expected values to adjust.
- Mark statements as observed fact, interpretation, assumption, decision, or unresolved gap when their status is not self-evident.
- Give rules, interfaces, tasks, oracle cases, risks, and decisions stable IDs that remain valid across slices.
- Cite immutable source by repository-relative path and precise line, statement, paragraph, job-step, or DDL-object range.
- Keep discovery, plans, architecture decisions, contracts, traceability, and validation evidence distinct even when they link to one another.
- Scope artifacts under `modernization/<application-id>/` and maintain its canonical `lifecycle.json` plus discovery, slice-plan, traceability, validation, deployment-plan, and deployment-report artifacts from `.github/templates/modernization/`.
- Keep application ID, source revision, slice ID, plan revision, contract revision, oracle-set revision, backend platform, target root, and target revision consistent across every linked index and handoff.
- Every slice plan must define scope, exclusions, dependencies, rule and oracle IDs, target mappings, acceptance gates, rollback, risks, and approval owners.
- Every slice plan must set `dataMigration.inScope`. In-scope plans require repository-bound mapping, aggregate profiling, migration, reconciliation, and recovery artifacts plus predeclared count/reject/control-total/hash tolerances. Out-of-scope plans require a reason and approved decision path; an empty object is not evidence.
- Keep source extracts, row-level rejects, backups, and production snapshots in approved protected storage. Store only sanitized aggregates, stable exception IDs, and protected-location references in Git.
- Every validation or deployment record must identify source, target, and applicable Terraform revisions; environment; commands; pass/fail/skip/blocked results; mismatches; approval references; and the narrowest supported verdict.
- Agents may set lifecycle state to draft, ready for review, implemented, passed, failed, or blocked as appropriate, but only an accountable human or external approval process may record an approval.
- Never put credentials, production records, access tokens, certificates, or unmasked protected data in modernization artifacts.