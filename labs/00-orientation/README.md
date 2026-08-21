# Lab 0: Orientation and prerequisites

**Outcome:** Understand the repository, prepare the required tools, and verify a safe
starting state without beginning modernization.

## What this repository teaches

This repository is a lab for evidence-first modernization of COBOL and related z/OS
artifacts into React, Azure SQL Database, and either Java/Spring Boot or .NET/ASP.NET
Core. It does not translate files
one by one. The process is:

```mermaid
flowchart LR
    E[Immutable legacy evidence] --> D[Discovery]
    D --> P[Slice planning]
    P --> I[Implementation]
    I --> V[Independent validation]
    V -->|findings| I
      V -->|passed gates| A[Approved Terraform deployment]
      A --> X[Independent Azure validation]
      X --> N[Next slice]
```

You learn that process while deconstructing the GitHub Copilot primitives that control
it. The Modernization Orchestrator is intentionally saved for the final lab.

## Documentation map

Read these documents in order:

1. The repository [README](../../README.md) explains the purpose, lifecycle, evidence
   standard, example applications, and security rules.
2. [HOW-TO-MODERNIZE](../../HOW-TO-MODERNIZE.md) is the concise operating guide for
   the completed customization system.
3. The [modernization workspace contract](../../modernization/README.md) defines where
   generated evidence, decisions, plans, and validation results belong.
4. The [lab index](../README.md) defines the learning path and completion standard.

Return to the focused lab instructions rather than using the operating guide as a
shortcut. The purpose is to understand why each primitive exists before orchestration.

## Repository map

| Path | Purpose | May learners or agents modify it? |
|---|---|---|
| `.github/copilot-instructions.md` | Always-on evidence, lifecycle, architecture, and security policy | Only when intentionally changing repository policy |
| `.github/instructions/` | Rules loaded for matching legacy, evidence, frontend, backend, database, local SQL, or E2E paths | Only when intentionally changing path policy |
| `.github/skills/` | Reusable specialist procedures with references and scripts | Yes, as a customization exercise |
| `.github/agents/` | Stage ownership, tools, boundaries, and handoffs | Yes, as a customization exercise |
| `.github/hooks/` | Deterministic tool-use enforcement | Only with regression tests |
| `.github/scripts/` | Lifecycle transition validation and tests | Only with regression tests |
| `.github/templates/modernization/` | Canonical lifecycle and artifact indexes | Edit templates, not approved generated evidence |
| `legacy-source/` | Immutable COBOL and mainframe forensic evidence | **Never** |
| `modernization/` | Generated analysis, plans, decisions, traceability, and validation evidence | Yes, through the owning lifecycle stage |
| `target/` | Generated React, selected Java or .NET backend, Azure SQL code, tests, and runbooks | Created and modified during approved implementation |
| `labs/` | The curriculum you are following | Only when maintaining the lab itself |

## Legacy application map

The extraction contains three examples under `legacy-source/DEV1/`:

| Application | Domain represented by the available evidence | Used in labs |
|---|---|---|
| `SURVDEMO` | Survivor inquiry, entitlement validation, and monthly benefit processing | Common application for Labs 1-16 |
| `BANKDEMO` | Account inquiry, transaction validation/posting, and daily processing | Capstone option |
| `TRSYDEMO` | Payment extraction and bank reconciliation | Capstone option |

Application subdirectories represent mainframe artifact types rather than target
layers. Depending on the application, they include:

- `COBOL/` programs and business behavior;
- `COPY/` shared record layouts and communication areas;
- `BMS/` CICS screen maps;
- `CSD/` CICS resource and transaction definitions;
- `DDL/` Db2 schemas;
- `JCL/` batch job control;
- `PROC/` reusable JCL procedures;
- `CNTL/` utility and sort control statements;
- `SCHED/` scheduler dependencies and timing relationships.

No single directory is the whole application. Discovery must connect online, batch,
data, interface, and operational evidence.

## GitHub Copilot prerequisites

Confirm that your VS Code and GitHub Copilot environment supports:

- workspace repository and path-specific instructions;
- workspace skills and their bundled resources;
- custom agents and agent handoffs;
- workspace tool use and pre-tool-use hooks.

Sign in with an account entitled to use GitHub Copilot. Open the repository root as the
VS Code workspace so `.github/` customizations are discoverable.

## Tool prerequisites

Labs 1-8 require:

- Git and a real Git worktree;
- Python 3;
- a shell capable of running the supplied Python checks.

Labs 9-14 additionally require the versions approved during planning for:

- Node.js and the selected package manager;
- either an LTS JDK and Java build wrapper, or a .NET LTS SDK pinned by `global.json`;
- Docker Desktop when using the local SQL Server inner loop;
- an approved Azure SQL environment for Azure compatibility or readiness claims.

Labs 15-16 additionally require Terraform, Azure access through Microsoft Entra,
protected remote state, an approved subscription/region, private DNS and network
ownership, and an approved private CI runner or operator path. CI/CD must use workload
identity federation. These labs do not use Azure Developer CLI (`azd`).

Real z/OS extraction and characterization require separate approved, least-privilege
access. The supplied extraction supports local discovery exercises but does not prove
live-system outcomes.

## Readiness checks

Run these non-destructive checks from the repository root:

```powershell
git rev-parse --show-toplevel
python --version
python -B .github/hooks/test_protect_legacy_source.py -v
python -B .github/scripts/test_validate_lifecycle.py -v
```

Before Lab 9, run the checks for the platform approved in Lab 7:

```powershell
node --version
docker version
java -version    # java-spring only
dotnet --info    # dotnet-aspnet-core only
```

The generated target README supplies the approved wrapper and package-manager commands.
Do not install or select both backend toolchains merely to complete one slice.

If Git does not identify this directory as a worktree, obtain or initialize the lab as
a versioned repository before lifecycle work. Source and target revisions are required
handoff identities, not optional labels.

## Safe starting state

Before a fresh run:

- `legacy-source/` contains the supplied immutable evidence;
- `modernization/` contains only its contract README;
- `target/` may not exist until the approved implementation lab;
- no credentials, production records, tokens, or unmasked protected data are present.

Do not delete a previous run casually. Preserve its modernization and target artifacts
as a branch, tag, commit, or separate lab copy before starting over.

## Verify

You are ready for Lab 1 when you can answer:

1. Which directory is immutable, and what enforces that rule?
2. Where do recovered evidence, approved plans, target code, and validation results go?
3. Which tools are needed now, and which can wait until implementation?
4. Why must the workspace be versioned before lifecycle handoffs?
5. Which application is shared by Labs 1-16?

**Exit criterion:** The readiness checks pass, the repository map is understood, and no
modernization or target artifact has been generated.

Continue to [Lab 1](../01-context-and-boundary/README.md).