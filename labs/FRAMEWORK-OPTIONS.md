# Backend framework options

The lab fixes React and Azure SQL but lets each approved slice choose one backend.
Framework choice happens during planning, is recorded in lifecycle state, and remains
bound through implementation, validation, and deployment.

## Supported choices

| Choice | Lifecycle identity | Target root | Specialist agent |
|---|---|---|---|
| Java and Spring Boot | `java-spring` | `target/react-spring-azure-sql` | Java Implementation Agent |
| .NET and ASP.NET Core | `dotnet-aspnet-core` | `target/react-dotnet-azure-sql` | Dotnet Implementation Agent |

“Latest” means the latest stable, organization-supported release at planning time. Use
an LTS runtime, select a compatible supported framework release, record its support end
date and upgrade owner, then pin the SDK/runtime, build tools, and dependencies. Do not
silently move to a newer minor or use a preview during implementation.

For the 2026 lab baseline, evaluate the current supported Java 25 LTS and Spring Boot
4.x lines against the current .NET 10 LTS and ASP.NET Core 10 line. Confirm exact
supported patch versions from official release/support documentation when the plan is
approved; the repository deliberately avoids hard-coding patch versions that age.

## How Copilot routes the choice

| Primitive | Purpose | Activation |
|---|---|---|
| Modernization Planner | Compares enterprise fit and writes the framework ADR | Planning stage |
| Lifecycle validator | Enforces a supported `backendPlatform`/`targetRoot` pair | Every transition from planning onward |
| Java Implementation Agent | Isolates Java/Spring implementation context and tools | Java handoff or orchestrator route |
| Dotnet Implementation Agent | Isolates C#/ASP.NET Core implementation context and tools | .NET handoff or orchestrator route |
| Java backend/database/local instructions | Apply Spring, Java, JDBC, migration, and test rules | Files under the Java target root |
| .NET backend/database/local instructions | Apply ASP.NET Core, C#, SqlClient, migration, and test rules | Files under the .NET target root |
| Shared React, E2E, infrastructure instructions | Keep contracts, UI, parity, and Terraform controls equivalent | Matching files under either target root |
| Shared implementation skill | Preserves the same evidence and component-gate sequence | Either implementation agent |
| Validation Critic | Checks platform identity and independently tests outcomes | Validation handoff |

Separate agents are appropriate because framework dependencies, build commands,
identity libraries, data-access choices, migration tooling, and test ecosystems differ.
Shared skills and gates are appropriate because recovered rules, OpenAPI behavior,
Azure SQL semantics, security outcomes, and parity evidence must not differ.

## Selection questions

Review these with application, platform, security, operations, and delivery owners:

- Which runtime/framework versions and support windows are approved?
- Which stack has established engineering, incident-response, and patching ownership?
- Do recovered batch restart/checkpoint semantics fit Spring Batch, .NET hosted services,
  or an external scheduler, and what evidence supports that fit?
- Does persistence require ORM productivity or exact SQL control?
- Are identity, observability, vulnerability management, SBOM, signing, and container
  baselines equally mature for both options?
- What coexistence adapters, vendor libraries, licensing constraints, and team skills
  materially change delivery risk or total cost?

Do not select by code-generation speed or build both implementations as a bake-off
inside one slice. A framework change creates a new plan revision and human approval.