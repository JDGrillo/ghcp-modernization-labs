# Lab 4: Hooks and deterministic enforcement

**Modernization outcome:** Demonstrate that legacy evidence cannot be mutated by agent tools  
**Copilot primitive:** Pre-tool-use hook

## Learn

Instructions guide model behavior. Hooks execute deterministic policy at lifecycle
events. This repository uses a `PreToolUse` hook to deny recognized mutations of
immutable evidence.

## Exercise

1. Inspect `.github/hooks/protect-legacy-source.json` and identify the event, command,
   and timeout.
2. Inspect `protect-legacy-source.py`. Find the read-only tools, mutating tools, path
   detection, terminal-command detection, and deny response.
3. Predict the result of each case in `test_protect_legacy_source.py`.
4. Run:

   ```powershell
   python -B .github/hooks/test_protect_legacy_source.py -v
   ```

5. Ask Copilot to explain why a terminal command mentioning the protected directory
   is denied even if the command appears to read a file.

## Verify

All hook tests pass. Explain the expected outcomes:

- dedicated read tool: allowed;
- patch or create under protected evidence: denied;
- terminal command referencing protected evidence: denied;
- unrelated terminal command: allowed.

## Explain

Why does the hook supplement rather than replace filesystem permissions and source
control review? Why is this invariant enforced by both instructions and a hook?

**Exit criterion:** You can name one policy suitable for instructions and one that
requires deterministic enforcement.

Continue to [Lab 5](../05-skills/README.md).