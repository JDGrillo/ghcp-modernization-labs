from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).with_name("protect-legacy-source.py")


def invoke_hook(payload: dict[str, object]) -> dict[str, object] | None:
    result = subprocess.run(
        [sys.executable, "-B", str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        check=True,
        text=True,
    )
    return json.loads(result.stdout) if result.stdout else None


class ProtectLegacySourceTests(unittest.TestCase):
    def assert_denied(self, payload: dict[str, object]) -> None:
        response = invoke_hook(payload)
        self.assertIsNotNone(response)
        output = response["hookSpecificOutput"]
        self.assertEqual("deny", output["permissionDecision"])

    def test_dedicated_read_tool_is_allowed(self) -> None:
        payload = {
            "tool_name": "read_file",
            "input": {"filePath": "legacy-source/APP/PROGRAM.cbl"},
        }
        self.assertIsNone(invoke_hook(payload))

    def test_patch_is_denied(self) -> None:
        payload = {
            "tool_name": "apply_patch",
            "input": {
                "input": "*** Update File: legacy-source/APP/PROGRAM.cbl\n-old\n+new"
            },
        }
        self.assert_denied(payload)

    def test_create_is_denied(self) -> None:
        payload = {
            "tool_name": "create_file",
            "input": {"filePath": "legacy-source/APP/new.cbl"},
        }
        self.assert_denied(payload)

    def test_terminal_remove_is_denied(self) -> None:
        payload = {
            "tool_name": "run_in_terminal",
            "input": {"command": "Remove-Item legacy-source/APP/PROGRAM.cbl"},
        }
        self.assert_denied(payload)

    def test_terminal_git_clean_is_denied(self) -> None:
        payload = {
            "tool_name": "run_in_terminal",
            "input": {"command": "git clean -fd ./legacy-source"},
        }
        self.assert_denied(payload)

    def test_terminal_absolute_windows_path_is_denied(self) -> None:
        payload = {
            "tool_name": "run_in_terminal",
            "input": {
                "command": (
                    "Remove-Item " "C:\\work\\repo\\LEGACY-SOURCE\\APP\\PROGRAM.cbl"
                )
            },
        }
        self.assert_denied(payload)

    def test_unrelated_terminal_command_is_allowed(self) -> None:
        payload = {
            "tool_name": "run_in_terminal",
            "input": {"command": "npm test"},
        }
        self.assertIsNone(invoke_hook(payload))


if __name__ == "__main__":
    unittest.main()
