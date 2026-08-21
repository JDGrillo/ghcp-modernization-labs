#!/usr/bin/env python3
"""Extract deterministic candidate evidence from COBOL and copybooks.

This is a conservative structural analyzer, not a COBOL compiler or runtime oracle.
Unsupported and unresolved constructs are reported rather than inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SOURCE_SUFFIXES = {".cbl", ".cob", ".cpy", ".copy", ".copybook"}
PARAGRAPH_EXCLUSIONS = {
    "CONFIGURATION SECTION",
    "FILE SECTION",
    "INPUT-OUTPUT SECTION",
    "LINKAGE SECTION",
    "LOCAL-STORAGE SECTION",
    "OBJECT-COMPUTER",
    "REPOSITORY",
    "SOURCE-COMPUTER",
    "WORKING-STORAGE SECTION",
}
CONTROL_TERMINATORS = {"GOBACK", "STOP RUN", "EXIT PROGRAM"}


@dataclass(frozen=True)
class SourceLine:
    number: int
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract deterministic candidate evidence from COBOL sources"
    )
    parser.add_argument("root", type=Path, help="Application source root")
    parser.add_argument("--output", type=Path, required=True, help="Analysis JSON path")
    parser.add_argument(
        "--source-revision", required=True, help="Immutable source revision"
    )
    parser.add_argument(
        "--application-id",
        required=True,
        help="Stable application ID, for example APP-SURVDEMO",
    )
    return parser.parse_args()


def stable_id(source_revision: str, path: str, kind: str, name: str, line: int) -> str:
    value = "|".join((source_revision, path, kind, name.upper(), str(line)))
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_lines(path: Path) -> list[SourceLine]:
    result: list[SourceLine] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if len(raw) >= 7 and raw[:6].strip().isdigit():
            indicator = raw[6]
            if indicator in {"*", "/"}:
                continue
            text = raw[7:72]
        else:
            stripped = raw.lstrip()
            if stripped.startswith("*"):
                continue
            text = raw
        text = text.rstrip()
        if text.strip():
            result.append(SourceLine(number, text))
    return result


def citation(relative_path: str, start: int, end: int | None = None) -> dict[str, Any]:
    return {
        "path": relative_path,
        "startLine": start,
        "endLine": end if end is not None else start,
    }


def blocks(lines: list[SourceLine], prefix: str) -> Iterable[list[SourceLine]]:
    current: list[SourceLine] = []
    active = False
    for line in lines:
        upper = line.text.upper()
        if not active and re.search(rf"\bEXEC\s+{prefix}\b", upper):
            active = True
            current = [line]
        elif active:
            current.append(line)
        if active and "END-EXEC" in upper:
            yield current
            active = False
            current = []
    if current:
        yield current


def parse_picture(picture: str, usage: str | None) -> dict[str, Any]:
    compact = picture.upper().replace(" ", "")
    signed = compact.startswith("S")
    numeric = "9" in compact and "X" not in compact and "A" not in compact
    scale = 0
    if "V" in compact:
        fractional = compact.split("V", 1)[1]
        scale = sum(
            int(count or "1") for count in re.findall(r"9(?:\((\d+)\))?", fractional)
        )
    digits = sum(int(count or "1") for count in re.findall(r"9(?:\((\d+)\))?", compact))
    length = sum(
        int(count or "1") for count in re.findall(r"[XAN9](?:\((\d+)\))?", compact)
    )
    edited = bool(re.search(r"[Z*$,+\-/]", compact))
    return {
        "picture": picture,
        "category": "numeric" if numeric else "alphanumeric",
        "digits": digits if numeric else None,
        "scale": scale if numeric else None,
        "signed": signed,
        "storage": usage or "DISPLAY",
        "declaredLength": length,
        "edited": edited,
    }


def diagnostic(
    code: str,
    severity: str,
    message: str,
    relative_path: str,
    line: int,
    subject: str,
) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "message": message,
        "subject": subject,
        "evidence": citation(relative_path, line),
    }


def analyze_file(
    root: Path,
    path: Path,
    source_revision: str,
    available_copybooks: set[str],
) -> dict[str, Any]:
    relative_path = path.relative_to(root).as_posix()
    lines = source_lines(path)
    program_id: str | None = None
    division = ""
    section = ""
    in_procedure = False
    current_paragraph: str | None = None
    copies: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    data_items: list[dict[str, Any]] = []
    paragraphs: list[dict[str, Any]] = []
    control_edges: list[dict[str, Any]] = []
    file_operations: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for line in lines:
        text = line.text.strip()
        upper = text.upper()
        program_match = re.search(r"\bPROGRAM-ID\.\s*([A-Z0-9-]+)", upper)
        if program_match:
            program_id = program_match.group(1)

        division_match = re.match(r"([A-Z-]+)\s+DIVISION\.", upper)
        if division_match:
            division = division_match.group(1)
            in_procedure = division == "PROCEDURE"
            section = ""
            continue
        section_match = re.match(r"([A-Z0-9-]+(?:\s+[A-Z0-9-]+)*)\s+SECTION\.", upper)
        if section_match:
            section = section_match.group(1)

        copy_match = re.search(r"\bCOPY\s+['\"]?([A-Z0-9@#$._-]+)", upper)
        if copy_match:
            name = copy_match.group(1).rstrip(".")
            resolved = name.upper() in available_copybooks
            copies.append(
                {
                    "id": stable_id(
                        source_revision, relative_path, "copy", name, line.number
                    ),
                    "name": name,
                    "resolved": resolved,
                    "evidence": citation(relative_path, line.number),
                }
            )
            if not resolved:
                diagnostics.append(
                    diagnostic(
                        "COBOL-COPY-UNRESOLVED",
                        "warning",
                        "Copybook was not found under the analyzed root",
                        relative_path,
                        line.number,
                        name,
                    )
                )

        if not in_procedure:
            data_match = re.match(
                r"(0?[1-9]|[1-4][0-9]|66|77|78|88)\s+([A-Z0-9-]+)\b(.*)", upper
            )
            if data_match:
                level, name, clauses = data_match.groups()
                picture_match = re.search(r"\bPIC(?:TURE)?\s+([^\s.]+)", clauses)
                usage_match = re.search(
                    r"\b(COMP(?:UTATIONAL)?(?:-[0-9])?|PACKED-DECIMAL|BINARY|DISPLAY)\b",
                    clauses,
                )
                redefines_match = re.search(r"\bREDEFINES\s+([A-Z0-9-]+)", clauses)
                occurs_match = re.search(
                    r"\bOCCURS\s+(\d+)(?:\s+TO\s+(\d+))?\s+TIMES(?:\s+DEPENDING\s+ON\s+([A-Z0-9-]+))?",
                    clauses,
                )
                value_match = re.search(r"\bVALUE(?:S)?\s+(.+?)(?:\.|$)", clauses)
                item: dict[str, Any] = {
                    "id": stable_id(
                        source_revision, relative_path, "data", name, line.number
                    ),
                    "level": int(level),
                    "name": name,
                    "division": division or None,
                    "section": section or None,
                    "redefines": redefines_match.group(1) if redefines_match else None,
                    "conditionValues": (
                        value_match.group(1).strip()
                        if level == "88" and value_match
                        else None
                    ),
                    "evidence": citation(relative_path, line.number),
                }
                if picture_match:
                    item.update(
                        parse_picture(
                            picture_match.group(1),
                            usage_match.group(1) if usage_match else None,
                        )
                    )
                    if item["edited"]:
                        diagnostics.append(
                            diagnostic(
                                "COBOL-PIC-EDITED",
                                "info",
                                "Edited PIC metadata is recorded but display semantics are not evaluated",
                                relative_path,
                                line.number,
                                name,
                            )
                        )
                else:
                    item.update(
                        {
                            "picture": None,
                            "category": (
                                "group"
                                if level not in {"66", "88"}
                                else "condition-or-rename"
                            ),
                            "digits": None,
                            "scale": None,
                            "signed": None,
                            "storage": None,
                            "declaredLength": None,
                            "edited": False,
                        }
                    )
                if occurs_match:
                    item["occurs"] = {
                        "minimum": int(occurs_match.group(1)),
                        "maximum": int(occurs_match.group(2) or occurs_match.group(1)),
                        "dependingOn": occurs_match.group(3),
                    }
                else:
                    item["occurs"] = None
                data_items.append(item)

        if in_procedure:
            paragraph_match = re.match(r"([A-Z0-9-]+)\.$", upper)
            if paragraph_match and upper not in PARAGRAPH_EXCLUSIONS:
                current_paragraph = paragraph_match.group(1)
                paragraphs.append(
                    {
                        "id": stable_id(
                            source_revision,
                            relative_path,
                            "paragraph",
                            current_paragraph,
                            line.number,
                        ),
                        "name": current_paragraph,
                        "evidence": citation(relative_path, line.number),
                    }
                )
                continue

            perform_match = re.search(
                r"\bPERFORM\s+([A-Z0-9-]+)(?:\s+(?:THRU|THROUGH)\s+([A-Z0-9-]+))?",
                upper,
            )
            if perform_match and perform_match.group(1) not in {
                "UNTIL",
                "VARYING",
                "WITH",
            }:
                target = perform_match.group(1)
                control_edges.append(
                    {
                        "type": "PERFORMS",
                        "from": current_paragraph,
                        "to": target,
                        "through": perform_match.group(2),
                        "evidence": citation(relative_path, line.number),
                    }
                )
            goto_match = re.search(r"\bGO\s+TO\s+([A-Z0-9-]+)", upper)
            if goto_match:
                control_edges.append(
                    {
                        "type": "GOES_TO",
                        "from": current_paragraph,
                        "to": goto_match.group(1),
                        "through": None,
                        "evidence": citation(relative_path, line.number),
                    }
                )
            call_match = re.search(r"\bCALL\s+([^\s.]+)", text, re.IGNORECASE)
            if call_match:
                raw_target = call_match.group(1)
                literal = raw_target.startswith(("'", '"'))
                target = raw_target.strip("'\"")
                calls.append(
                    {
                        "id": stable_id(
                            source_revision, relative_path, "call", target, line.number
                        ),
                        "target": target,
                        "resolution": "static" if literal else "dynamic-unresolved",
                        "evidence": citation(relative_path, line.number),
                    }
                )
                if not literal:
                    diagnostics.append(
                        diagnostic(
                            "COBOL-CALL-DYNAMIC",
                            "warning",
                            "Dynamic call target requires source or runtime reconciliation",
                            relative_path,
                            line.number,
                            target,
                        )
                    )
            file_match = re.match(
                r"(READ|WRITE|REWRITE|DELETE|OPEN|CLOSE)\s+([A-Z0-9-]+)", upper
            )
            if file_match:
                file_operations.append(
                    {
                        "operation": file_match.group(1),
                        "subject": file_match.group(2),
                        "paragraph": current_paragraph,
                        "evidence": citation(relative_path, line.number),
                    }
                )

    paragraph_names = {paragraph["name"] for paragraph in paragraphs}
    for previous, following in zip(paragraphs, paragraphs[1:]):
        control_edges.append(
            {
                "type": "FALLS_THROUGH",
                "from": previous["name"],
                "to": following["name"],
                "through": None,
                "evidence": previous["evidence"],
            }
        )
    for edge in control_edges:
        if edge["to"] not in paragraph_names:
            diagnostics.append(
                diagnostic(
                    "COBOL-FLOW-TARGET-UNRESOLVED",
                    "warning",
                    "Control-flow target was not found in this source file",
                    relative_path,
                    edge["evidence"]["startLine"],
                    edge["to"],
                )
            )

    sql_operations: list[dict[str, Any]] = []
    for block in blocks(lines, "SQL"):
        joined = " ".join(item.text.strip() for item in block)
        body = re.sub(r".*?EXEC\s+SQL\s+", "", joined, flags=re.IGNORECASE)
        body = re.sub(r"\s+END-EXEC.*", "", body, flags=re.IGNORECASE)
        operation_match = re.search(
            r"\b(SELECT|INSERT|UPDATE|DELETE|DECLARE|OPEN|FETCH|CLOSE|COMMIT|ROLLBACK|INCLUDE)\b",
            body,
            re.IGNORECASE,
        )
        operation = operation_match.group(1).upper() if operation_match else "UNKNOWN"
        tables = sorted(
            {
                match.upper()
                for match in re.findall(
                    r"\b(?:FROM|JOIN|UPDATE|INSERT\s+INTO|DELETE\s+FROM)\s+([A-Z0-9_.-]+)",
                    body,
                    re.IGNORECASE,
                )
            }
        )
        sql_operations.append(
            {
                "id": stable_id(
                    source_revision, relative_path, "sql", operation, block[0].number
                ),
                "operation": operation,
                "tables": tables,
                "evidence": citation(relative_path, block[0].number, block[-1].number),
            }
        )

    cics_operations: list[dict[str, Any]] = []
    for block in blocks(lines, "CICS"):
        joined = " ".join(item.text.strip() for item in block)
        body = re.sub(r".*?EXEC\s+CICS\s+", "", joined, flags=re.IGNORECASE)
        body = re.sub(r"\s+END-EXEC.*", "", body, flags=re.IGNORECASE)
        action_match = re.match(r"([A-Z-]+)", body.strip(), re.IGNORECASE)
        action = action_match.group(1).upper() if action_match else "UNKNOWN"
        resources = {
            key.upper(): value
            for key, value in re.findall(
                r"\b(MAP|MAPSET|TRANSID|PROGRAM|FILE|QUEUE|DATASET)\s*\(\s*['\"]?([A-Z0-9@#$._-]+)",
                body,
                re.IGNORECASE,
            )
        }
        cics_operations.append(
            {
                "id": stable_id(
                    source_revision, relative_path, "cics", action, block[0].number
                ),
                "operation": action,
                "resources": resources,
                "evidence": citation(relative_path, block[0].number, block[-1].number),
            }
        )

    status = (
        "partial"
        if any(item["severity"] == "warning" for item in diagnostics)
        else "succeeded"
    )
    return {
        "path": relative_path,
        "sha256": sha256_file(path),
        "kind": (
            "copybook" if path.suffix.lower() not in {".cbl", ".cob"} else "program"
        ),
        "programId": program_id,
        "status": status,
        "copies": copies,
        "calls": calls,
        "dataItems": data_items,
        "paragraphs": paragraphs,
        "paragraphControlFlow": control_edges,
        "sqlOperations": sql_operations,
        "cicsOperations": cics_operations,
        "fileOperations": file_operations,
        "diagnostics": diagnostics,
    }


def analyze(root: Path, application_id: str, source_revision: str) -> dict[str, Any]:
    files = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    available_copybooks = {
        path.stem.upper()
        for path in files
        if path.suffix.lower() not in {".cbl", ".cob"}
    }
    results = [
        analyze_file(root, path, source_revision, available_copybooks) for path in files
    ]
    status_counts = Counter(result["status"] for result in results)
    diagnostic_counts = Counter(
        item["severity"] for result in results for item in result["diagnostics"]
    )
    return {
        "schemaVersion": 1,
        "artifactType": "automated-cobol-analysis",
        "applicationId": application_id,
        "sourceRevision": source_revision,
        "analyzer": {
            "name": "modernization-lab-cobol-structural-analyzer",
            "version": "1.0.0",
            "capability": "candidate-evidence-only",
        },
        "coverage": {
            "attempted": len(results),
            "succeeded": status_counts["succeeded"],
            "partial": status_counts["partial"],
            "failed": status_counts["failed"],
            "warningCount": diagnostic_counts["warning"],
            "errorCount": diagnostic_counts["error"],
        },
        "limitations": [
            "This artifact is candidate structural evidence, not approved business behavior.",
            "Paragraph control flow does not model statement-level branch paths or runtime reachability.",
            "PIC metadata does not prove runtime representation, encoding, or display behavior.",
            "Dynamic calls and missing copybooks require independent reconciliation.",
            "SQL and CICS extraction identifies operations and named resources, not transactional semantics.",
        ],
        "files": results,
    }


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: source root is not a directory: {root}", file=sys.stderr)
        return 2
    if not re.fullmatch(r"APP-[A-Z0-9-]+", args.application_id):
        print("error: --application-id must match APP-[A-Z0-9-]+", file=sys.stderr)
        return 2
    result = analyze(root, args.application_id, args.source_revision)
    if result["coverage"]["attempted"] == 0:
        print(f"error: no COBOL or copybook files found under {root}", file=sys.stderr)
        return 3
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    coverage = result["coverage"]
    print(
        "Analyzed "
        f"{coverage['attempted']} files: {coverage['succeeded']} succeeded, "
        f"{coverage['partial']} partial, {coverage['failed']} failed; output {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
