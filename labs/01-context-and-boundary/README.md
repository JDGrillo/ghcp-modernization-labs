# Lab 1: Context and the evidence boundary

**Modernization outcome:** A precise `SURVDEMO` analysis boundary  
**Copilot concept:** Workspace context, explicit context, and effective requests

**Prerequisite:** Complete [Lab 0](../00-orientation/README.md) without generating
modernization or target artifacts.

## Learn

Copilot can search a workspace, but it should not decide an ambiguous application
boundary or invent unavailable mainframe evidence. A useful request identifies the
subject, task, constraints, exclusions, and expected output.

## Exercise

1. Start a new chat with the default agent.
2. Ask: `Modernize this mainframe application.`
3. Record which application, capability, evidence, and output location are ambiguous.
4. Inspect the `SURVDEMO` directories without asking for target design.
5. Submit this bounded request:

   ```text
   Inspect legacy-source/DEV1/SURVDEMO as immutable evidence. Identify the
   available artifact types and candidate entry points. Separate observed facts,
   interpretations, and unresolved gaps. Do not edit files, recover detailed
   business rules, select an MVP, or design target code. Return the result in chat.
   ```

6. Compare the two responses. Identify which improvements came from explicit user
   context and which came from repository policy.

## Verify

The bounded response must:

- stay within `SURVDEMO`;
- identify multiple artifact types rather than COBOL alone;
- avoid target architecture and implementation;
- label uncertainty rather than filling gaps.

## Explain

Answer before continuing: why should the application boundary be in the request or
lifecycle manifest rather than buried in a skill?

**Exit criterion:** You can state the application boundary, explicit exclusions, and
the evidence needed before detailed discovery.

Continue to [Lab 2](../02-repository-instructions/README.md).