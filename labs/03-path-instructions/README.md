# Lab 3: Path-specific instructions

**Modernization outcome:** Apply evidence and technology rules to the files they govern  
**Copilot primitive:** `.github/instructions/*.instructions.md`

## Learn

Path instructions load when matching files are involved. Their `applyTo` globs keep
legacy preservation, evidence-writing, React, Java/Spring, .NET/ASP.NET Core, database, local SQL, and E2E
rules out of unrelated contexts.

## Exercise

1. Inspect the frontmatter and body of:
   - `legacy-source.instructions.md`;
   - `modernization-artifacts.instructions.md`;
   - `react-frontend.instructions.md`;
   - `react-spring-backend.instructions.md`;
   - `react-dotnet-backend.instructions.md`;
   - the matching Java or .NET database instructions.
2. For each file, write one sample path that matches and one that does not.
3. Focus a COBOL file and ask which constraints govern an analysis of that file.
4. Focus the modernization contract and ask which metadata must remain consistent.
5. Compare the frontend and backend rules for money, authorization, and business rules.

## Verify

Complete this decision table:

| Work item | Instructions that should apply |
|---|---|
| Cite a COBOL rule | Repository + legacy source |
| Edit a lifecycle manifest | Repository + modernization artifacts |
| Add a Flyway migration | Repository + stack + backend/database |
| Add an EF Core migration | Repository + .NET stack + .NET backend/database |
| Add a React error state | Repository + stack + frontend |

## Explain

Why is `applyTo: "**"` inappropriate for the database instruction file?

**Exit criterion:** You can use the `applyTo` declarations to identify the instruction
set for a proposed file path.

Continue to [Lab 4](../04-hooks-and-enforcement/README.md).