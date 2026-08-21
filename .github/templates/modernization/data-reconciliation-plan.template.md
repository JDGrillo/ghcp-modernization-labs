# Data Reconciliation Plan

Bind every comparison to the same immutable source snapshot and target migration run. Define canonicalization before hashing, including encoding, collation, padding, null/blank, decimal scale, and date/time behavior.

## Required Comparisons

- Row counts by object and approved business partition.
- Distinct and duplicate key counts.
- Monetary and other business control totals using exact decimals.
- Canonical hashes where they provide meaningful coverage.
- Null, blank, sentinel, code-frequency, orphan, and rejected-row counts.
- Approved sampled field-level comparisons that do not expose protected data.

State numeric tolerances before execution. Default row-count and rejected-row tolerances to zero. Every exception needs a stable ID, affected keys represented safely, owner, rationale, approval, and disposition. A migration command exiting successfully is not reconciliation evidence.