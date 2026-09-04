# Lab 4: Hooks and deterministic enforcement

**Modernization outcome:** Demonstrate that legacy evidence cannot be mutated by agent tools  
**Copilot primitive:** Pre-tool-use hook

## Learn

Instructions guide model behavior. Hooks execute deterministic policy at lifecycle
events. This repository uses a `PreToolUse` hook to deny recognized mutations of
immutable evidence.

The demo uses three connected artifacts:

| Artifact | Role in the demo |
|---|---|
| [Hook configuration](../../.github/hooks/protect-legacy-source.json) | Registers the `PreToolUse` event, command, and timeout |
| [Hook implementation](../../.github/hooks/protect-legacy-source.py) | Classifies tools and paths and returns allow or deny responses |
| [Hook regression suite](../../.github/hooks/test_protect_legacy_source.py) | Defines allowed reads, denied mutations, conservative terminal handling, and unrelated commands |

## Exercise

1. Inspect the hook configuration and connect its event, command, and timeout to the
   implementation.
2. In the implementation, locate the read-only tools, mutating tools, path detection,
   terminal-command detection, and deny response.
3. Read the regression suite as the executable behavior contract. Map each test to
   one of the expected outcomes listed under **Verify**. The suite has seven cases:
   one dedicated read, two direct file mutations, three protected-path terminal
   commands, and one unrelated terminal command.
4. Run:

   ```powershell
   python -B .github/hooks/test_protect_legacy_source.py -v
   ```

5. Use this demo prompt:

   ```text
   Using the hook configuration, implementation, and tests, explain why a terminal
   command mentioning legacy-source is denied even when it appears read-only. Cite
   the deterministic behavior that the regression suite verifies.
   ```

## Verify

The command exits with code 0 and reports 7 passing tests. Explain the expected
outcomes:

- dedicated read tool: allowed;
- patch or create under protected evidence: denied by both tested direct mutation
  paths;
- terminal command referencing protected evidence: denied for relative, `git clean`,
  and absolute Windows-path cases;
- unrelated terminal command: allowed.

## Explain

Why does the hook supplement rather than replace filesystem permissions and source
control review? Why is this invariant enforced by both instructions and a hook? Why
does this repository conservatively deny every terminal command that references
`legacy-source/`, including apparently read-only commands, while allowing dedicated
read/search tools?

**Exit criterion:** You can name one policy suitable for instructions and one that
requires deterministic enforcement.

Continue to [Lab 5](../05-skills/README.md).