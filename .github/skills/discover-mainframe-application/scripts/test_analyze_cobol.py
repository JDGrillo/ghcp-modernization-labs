from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from analyze_cobol import analyze

PROGRAM = """\
000100 IDENTIFICATION DIVISION.
000200 PROGRAM-ID. SAMPLE.
000300 DATA DIVISION.
000400 WORKING-STORAGE SECTION.
000500 01 TOTAL-AMOUNT PIC S9(7)V99 COMP-3.
000600 01 STATUS-CODE PIC X.
000700    88 STATUS-OPEN VALUE 'O'.
000800    COPY RECORDS.
000900 PROCEDURE DIVISION.
001000 MAIN-LOGIC.
001100    PERFORM LOAD-DATA
001200    CALL 'VALIDATE'
001300    EXEC SQL SELECT AMOUNT FROM APP.PAYMENT END-EXEC
001400    EXEC CICS RETURN TRANSID('SA01') END-EXEC.
001500 LOAD-DATA.
001600    READ INPUT-FILE
001700    GO TO FINISH.
001800 FINISH.
001900    GOBACK.
"""

COPYBOOK = """\
000100 01 INPUT-RECORD.
000200    05 INPUT-ID PIC X(10).
"""


class AnalyzeCobolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "SAMPLE.cbl").write_text(PROGRAM, encoding="utf-8")
        (self.root / "RECORDS.cpy").write_text(COPYBOOK, encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_extracts_high_value_candidate_evidence(self) -> None:
        result = analyze(self.root, "APP-SAMPLE", "source-1")
        program = next(item for item in result["files"] if item["kind"] == "program")

        self.assertEqual("SAMPLE", program["programId"])
        self.assertEqual(True, program["copies"][0]["resolved"])
        self.assertEqual("static", program["calls"][0]["resolution"])
        amount = next(
            item for item in program["dataItems"] if item["name"] == "TOTAL-AMOUNT"
        )
        self.assertEqual(
            (9, 2, True, "COMP-3"),
            (amount["digits"], amount["scale"], amount["signed"], amount["storage"]),
        )
        self.assertEqual(["APP.PAYMENT"], program["sqlOperations"][0]["tables"])
        self.assertEqual("SA01", program["cicsOperations"][0]["resources"]["TRANSID"])
        self.assertTrue(
            any(
                edge["type"] == "PERFORMS" and edge["to"] == "LOAD-DATA"
                for edge in program["paragraphControlFlow"]
            )
        )
        self.assertTrue(
            any(
                edge["type"] == "GOES_TO" and edge["to"] == "FINISH"
                for edge in program["paragraphControlFlow"]
            )
        )

    def test_output_is_deterministic(self) -> None:
        first = analyze(self.root, "APP-SAMPLE", "source-1")
        second = analyze(self.root, "APP-SAMPLE", "source-1")

        self.assertEqual(
            json.dumps(first, sort_keys=True),
            json.dumps(second, sort_keys=True),
        )

    def test_unresolved_dependencies_are_explicit_and_partial(self) -> None:
        (self.root / "SAMPLE.cbl").write_text(
            PROGRAM.replace("COPY RECORDS", "COPY MISSING").replace(
                "CALL 'VALIDATE'", "CALL WS-TARGET"
            ),
            encoding="utf-8",
        )

        result = analyze(self.root, "APP-SAMPLE", "source-1")
        program = next(item for item in result["files"] if item["kind"] == "program")
        codes = {item["code"] for item in program["diagnostics"]}

        self.assertEqual("partial", program["status"])
        self.assertIn("COBOL-COPY-UNRESOLVED", codes)
        self.assertIn("COBOL-CALL-DYNAMIC", codes)

    def test_repository_samples_are_analyzable_and_deterministic(self) -> None:
        repository_root = Path(__file__).resolve().parents[4]
        source_root = repository_root / "legacy-source" / "DEV1"

        for application in ("BANKDEMO", "SURVDEMO", "TRSYDEMO"):
            with self.subTest(application=application):
                first = analyze(
                    source_root / application,
                    f"APP-{application}",
                    "test-source-revision",
                )
                second = analyze(
                    source_root / application,
                    f"APP-{application}",
                    "test-source-revision",
                )
                self.assertGreater(first["coverage"]["attempted"], 0)
                self.assertEqual(0, first["coverage"]["failed"])
                self.assertEqual(
                    json.dumps(first, sort_keys=True),
                    json.dumps(second, sort_keys=True),
                )


if __name__ == "__main__":
    unittest.main()
