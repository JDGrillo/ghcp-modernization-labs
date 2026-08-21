#!/usr/bin/env python3
"""Validate modernization lifecycle state before an agent handoff."""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

TRANSITIONS = {
    "to-planning": {
        "stage": "discovery",
        "status": "approved",
        "artifacts": ("discoveryIndex",),
        "approval": True,
        "activeSlice": False,
    },
    "to-implementation": {
        "stage": "planning",
        "status": "approved",
        "artifacts": ("discoveryIndex", "slicePlanIndex", "traceabilityIndex"),
        "approval": True,
        "activeSlice": True,
    },
    "to-validation": {
        "stage": "implementation",
        "status": "implemented",
        "artifacts": (
            "discoveryIndex",
            "slicePlanIndex",
            "traceabilityIndex",
            "implementationReport",
        ),
        "approval": False,
        "activeSlice": True,
    },
    "to-deployment-plan": {
        "stage": "validation",
        "status": "passed",
        "artifacts": ("slicePlanIndex", "validationGateReport"),
        "approval": False,
        "activeSlice": True,
    },
    "to-deployment-apply": {
        "stage": "deployment",
        "status": "planned",
        "artifacts": ("slicePlanIndex", "deploymentPlan"),
        "approval": True,
        "activeSlice": True,
    },
    "to-azure-validation": {
        "stage": "deployment",
        "status": "deployed",
        "artifacts": ("slicePlanIndex", "deploymentPlan", "deploymentReport"),
        "approval": False,
        "activeSlice": True,
    },
    "to-next-slice": {
        "stage": "validation",
        "status": "passed",
        "artifacts": ("slicePlanIndex", "validationGateReport"),
        "approval": False,
        "activeSlice": True,
    },
}

ACTIVE_SLICE_FIELDS = (
    "sliceId",
    "planRevision",
    "contractRevision",
    "oracleSetRevision",
    "backendPlatform",
    "targetRoot",
)
BACKEND_TARGETS = {
    "java-spring": "target/react-spring-azure-sql",
    "dotnet-aspnet-core": "target/react-dotnet-azure-sql",
}
TARGET_TRANSITIONS = {
    "to-validation",
    "to-deployment-plan",
    "to-deployment-apply",
    "to-azure-validation",
    "to-next-slice",
}
ARTIFACT_TYPES = {
    "discoveryIndex": "discovery-index",
    "slicePlanIndex": "slice-plan-index",
    "traceabilityIndex": "traceability-index",
    "implementationReport": "implementation-report",
    "validationGateReport": "validation-gate-report",
    "deploymentPlan": "deployment-plan",
    "deploymentReport": "deployment-report",
}
SLICE_ARTIFACTS = {
    "slicePlanIndex",
    "traceabilityIndex",
    "implementationReport",
    "validationGateReport",
    "deploymentPlan",
    "deploymentReport",
}
DATA_MIGRATION_PATH_FIELDS = (
    "sourceToTargetMapPath",
    "dataProfilePath",
    "migrationRunbookPath",
    "reconciliationPlanPath",
    "recoveryRunbookPath",
)


def validate_automated_analysis(
    discovery_index: dict[str, Any], root: Path, errors: list[str]
) -> None:
    declaration = discovery_index.get("automatedAnalysis")
    if declaration is None:
        return
    prefix = "artifacts.discoveryIndex automatedAnalysis"
    if not isinstance(declaration, dict):
        errors.append(f"{prefix} must be an object")
        return
    in_scope = declaration.get("inScope")
    if not isinstance(in_scope, bool):
        errors.append(f"{prefix}.inScope must be a boolean")
        return
    if not in_scope:
        require_text(
            declaration.get("notApplicableReason"),
            f"{prefix}.notApplicableReason",
            errors,
        )
        return

    artifact_path = declaration.get("artifactPath")
    reconciliation_path = declaration.get("reconciliationPath")
    validate_repository_file(artifact_path, f"{prefix}.artifactPath", root, errors)
    validate_repository_file(
        reconciliation_path, f"{prefix}.reconciliationPath", root, errors
    )
    if not isinstance(artifact_path, str) or not artifact_path.strip():
        return
    expected_root = (
        f"modernization/{discovery_index.get('applicationId')}/"
        "evidence/automated-analysis/"
    )
    if not artifact_path.replace("\\", "/").startswith(expected_root):
        errors.append(f"{prefix}.artifactPath must be under {expected_root}")
    resolved = (root / artifact_path).resolve()
    if not resolved.is_file():
        return
    try:
        artifact = load_json(resolved)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        errors.append(f"{prefix}.artifactPath is invalid JSON: {error}")
        return
    for field, expected in (
        ("schemaVersion", 1),
        ("artifactType", "automated-cobol-analysis"),
        ("applicationId", discovery_index.get("applicationId")),
        ("sourceRevision", discovery_index.get("sourceRevision")),
    ):
        if artifact.get(field) != expected:
            errors.append(f"{prefix} artifact {field} must match {expected!r}")
    analyzer = artifact.get("analyzer")
    if not isinstance(analyzer, dict):
        errors.append(f"{prefix} artifact analyzer must be an object")
    elif analyzer.get("capability") != "candidate-evidence-only":
        errors.append(
            f"{prefix} artifact analyzer.capability must be 'candidate-evidence-only'"
        )
    coverage = artifact.get("coverage")
    if not isinstance(coverage, dict):
        errors.append(f"{prefix} artifact coverage must be an object")
    else:
        for field in ("attempted", "succeeded", "partial", "failed", "errorCount"):
            value = coverage.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(
                    f"{prefix} artifact coverage.{field} must be a non-negative integer"
                )
        if coverage.get("failed") != 0:
            errors.append(f"{prefix} artifact coverage.failed must be 0")
        if coverage.get("errorCount") != 0:
            errors.append(f"{prefix} artifact coverage.errorCount must be 0")
        files = artifact.get("files")
        if isinstance(files, list) and isinstance(coverage.get("attempted"), int):
            if len(files) != coverage["attempted"]:
                errors.append(
                    f"{prefix} artifact coverage.attempted must equal files length"
                )
    if not isinstance(artifact.get("files"), list):
        errors.append(f"{prefix} artifact files must be an array")
    limitations = artifact.get("limitations")
    if not isinstance(limitations, list) or not limitations:
        errors.append(f"{prefix} artifact limitations must be a non-empty array")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("manifest root must be a JSON object")
    return value


def repository_root(manifest_path: Path) -> Path:
    for parent in (manifest_path.parent, *manifest_path.parents):
        if (parent / ".github").is_dir() and (parent / "modernization").is_dir():
            return parent
    raise ValueError("manifest is not inside a modernization repository")


def require_text(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")


def validate_repository_file(
    value: Any,
    field: str,
    root: Path,
    errors: list[str],
) -> None:
    require_text(value, field, errors)
    if not isinstance(value, str) or not value.strip():
        return
    resolved = (root / value).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{field} must stay inside the repository")
        return
    if not resolved.is_file():
        errors.append(f"{field} does not exist: {value}")


def validate_data_migration(
    artifact: dict[str, Any], root: Path, errors: list[str]
) -> None:
    prefix = "artifacts.slicePlanIndex dataMigration"
    data_migration = artifact.get("dataMigration")
    if not isinstance(data_migration, dict):
        errors.append(f"{prefix} must be an object")
        return

    in_scope = data_migration.get("inScope")
    if not isinstance(in_scope, bool):
        errors.append(f"{prefix}.inScope must be a boolean")
        return
    if not in_scope:
        require_text(
            data_migration.get("notApplicableReason"),
            f"{prefix}.notApplicableReason",
            errors,
        )
        validate_repository_file(
            data_migration.get("approvedDecisionPath"),
            f"{prefix}.approvedDecisionPath",
            root,
            errors,
        )
        return

    for field in DATA_MIGRATION_PATH_FIELDS:
        validate_repository_file(
            data_migration.get(field), f"{prefix}.{field}", root, errors
        )
    require_text(
        data_migration.get("sourceSnapshotReference"),
        f"{prefix}.sourceSnapshotReference",
        errors,
    )

    reconciliation = data_migration.get("reconciliation")
    if not isinstance(reconciliation, dict):
        errors.append(f"{prefix}.reconciliation must be an object")
    else:
        for field in ("rowCountTolerance", "rejectedRowTolerance"):
            value = reconciliation.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(
                    f"{prefix}.reconciliation.{field} must be a non-negative integer"
                )
        control_total_tolerance = reconciliation.get("controlTotalTolerance")
        require_text(
            control_total_tolerance,
            f"{prefix}.reconciliation.controlTotalTolerance",
            errors,
        )
        if isinstance(control_total_tolerance, str) and control_total_tolerance.strip():
            try:
                decimal_tolerance = Decimal(control_total_tolerance)
                if not decimal_tolerance.is_finite() or decimal_tolerance < 0:
                    raise InvalidOperation
            except InvalidOperation:
                errors.append(
                    f"{prefix}.reconciliation.controlTotalTolerance must be a "
                    "non-negative exact decimal string"
                )
        require_text(
            reconciliation.get("hashMethod"),
            f"{prefix}.reconciliation.hashMethod",
            errors,
        )

    recovery_mode = data_migration.get("recoveryMode")
    if recovery_mode not in {"rollback", "forward-recovery"}:
        errors.append(f"{prefix}.recoveryMode must be 'rollback' or 'forward-recovery'")


def validate_data_gate_artifacts(
    artifacts: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    slice_plan = artifacts.get("slicePlanIndex")
    if not isinstance(slice_plan, dict):
        return
    data_migration = slice_plan.get("dataMigration")
    if (
        not isinstance(data_migration, dict)
        or data_migration.get("inScope") is not True
    ):
        return

    validation_report = artifacts.get("validationGateReport")
    if isinstance(validation_report, dict):
        prefix = "artifacts.validationGateReport dataMigrationEvidence"
        evidence = validation_report.get("dataMigrationEvidence")
        if not isinstance(evidence, dict):
            errors.append(f"{prefix} must be an object")
        else:
            require_text(
                evidence.get("sourceSnapshotIdentity"),
                f"{prefix}.sourceSnapshotIdentity",
                errors,
            )
            if evidence.get("sourceSnapshotIdentity") != data_migration.get(
                "sourceSnapshotReference"
            ):
                errors.append(f"{prefix}.sourceSnapshotIdentity must match slice plan")
            for field in (
                "schemaMigrationResult",
                "dataReconciliationResult",
                "rejectReconciliationResult",
                "recoveryRehearsalResult",
            ):
                if evidence.get(field) != "passed":
                    errors.append(f"{prefix}.{field} must be 'passed'")
            if not isinstance(evidence.get("exceptions"), list):
                errors.append(f"{prefix}.exceptions must be an array")

    deployment_plan = artifacts.get("deploymentPlan")
    if isinstance(deployment_plan, dict):
        prefix = "artifacts.deploymentPlan databaseChange"
        database_change = deployment_plan.get("databaseChange")
        if not isinstance(database_change, dict):
            errors.append(f"{prefix} must be an object")
        else:
            for field in (
                "migrationRevision",
                "sourceSnapshotReference",
                "preMigrationBackupReference",
                "restoreRehearsalReference",
                "reconciliationPlanPath",
                "recoveryRunbookPath",
            ):
                require_text(database_change.get(field), f"{prefix}.{field}", errors)
            if database_change.get("sourceSnapshotReference") != data_migration.get(
                "sourceSnapshotReference"
            ):
                errors.append(f"{prefix}.sourceSnapshotReference must match slice plan")
            for plan_field, migration_field in (
                ("reconciliationPlanPath", "reconciliationPlanPath"),
                ("recoveryRunbookPath", "recoveryRunbookPath"),
            ):
                if database_change.get(plan_field) != data_migration.get(
                    migration_field
                ):
                    errors.append(f"{prefix}.{plan_field} must match slice plan")

    deployment_report = artifacts.get("deploymentReport")
    if isinstance(deployment_report, dict):
        prefix = "artifacts.deploymentReport dataReconciliation"
        reconciliation_result = deployment_report.get("dataReconciliation")
        if not isinstance(reconciliation_result, dict):
            errors.append(f"{prefix} must be an object")
        else:
            require_text(
                reconciliation_result.get("sourceSnapshotReference"),
                f"{prefix}.sourceSnapshotReference",
                errors,
            )
            for field in ("rowCountResult", "controlTotalResult", "hashResult"):
                if reconciliation_result.get(field) != "passed":
                    errors.append(f"{prefix}.{field} must be 'passed'")
            rejected_row_count = reconciliation_result.get("rejectedRowCount")
            tolerance = data_migration.get("reconciliation", {}).get(
                "rejectedRowTolerance"
            )
            if (
                not isinstance(rejected_row_count, int)
                or isinstance(rejected_row_count, bool)
                or rejected_row_count < 0
            ):
                errors.append(
                    f"{prefix}.rejectedRowCount must be a non-negative integer"
                )
            elif isinstance(tolerance, int) and rejected_row_count > tolerance:
                errors.append(
                    f"{prefix}.rejectedRowCount exceeds approved tolerance {tolerance}"
                )
            if not isinstance(reconciliation_result.get("exceptionReferences"), list):
                errors.append(f"{prefix}.exceptionReferences must be an array")

        database_change = (
            deployment_plan.get("databaseChange")
            if isinstance(deployment_plan, dict)
            else None
        )
        if isinstance(database_change, dict) and isinstance(
            reconciliation_result, dict
        ):
            if reconciliation_result.get(
                "sourceSnapshotReference"
            ) != database_change.get("sourceSnapshotReference"):
                errors.append(
                    f"{prefix}.sourceSnapshotReference must match deployment plan"
                )
            if reconciliation_result.get(
                "sourceSnapshotReference"
            ) != data_migration.get("sourceSnapshotReference"):
                errors.append(f"{prefix}.sourceSnapshotReference must match slice plan")


def validate_artifact_identity(
    artifact: dict[str, Any],
    artifact_field: str,
    manifest: dict[str, Any],
    errors: list[str],
) -> None:
    expected: dict[str, Any] = {
        "schemaVersion": 1,
        "artifactType": ARTIFACT_TYPES[artifact_field],
        "applicationId": manifest.get("applicationId"),
        "sourceRevision": manifest.get("sourceRevision"),
    }
    active_slice = manifest.get("activeSlice")
    if artifact_field in SLICE_ARTIFACTS and isinstance(active_slice, dict):
        for field in ACTIVE_SLICE_FIELDS:
            expected[field] = active_slice.get(field)
        if artifact_field in {
            "implementationReport",
            "validationGateReport",
            "deploymentPlan",
            "deploymentReport",
        }:
            expected["targetRevision"] = active_slice.get("targetRevision")

    for field, expected_value in expected.items():
        if artifact.get(field) != expected_value:
            errors.append(
                f"artifacts.{artifact_field} {field} must match lifecycle value "
                f"{expected_value!r}"
            )


def validate_manifest(
    manifest: dict[str, Any], manifest_path: Path, transition: str
) -> list[str]:
    errors: list[str] = []
    rule = TRANSITIONS[transition]

    if manifest.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    require_text(manifest.get("applicationId"), "applicationId", errors)
    require_text(manifest.get("sourceRevision"), "sourceRevision", errors)
    if manifest.get("currentStage") != rule["stage"]:
        errors.append(f"currentStage must be {rule['stage']!r} for {transition}")
    if manifest.get("status") != rule["status"]:
        errors.append(f"status must be {rule['status']!r} for {transition}")

    gaps = manifest.get("criticalGaps")
    if not isinstance(gaps, list):
        errors.append("criticalGaps must be an array")
    elif gaps:
        errors.append("criticalGaps must be empty before a lifecycle transition")

    approval = manifest.get("approval")
    if rule["approval"]:
        if not isinstance(approval, dict) or approval.get("decision") != "approved":
            errors.append("approval.decision must be 'approved'")
        else:
            for field in ("approvedBy", "approvedAt", "decisionReference"):
                require_text(approval.get(field), f"approval.{field}", errors)

    active_slice = manifest.get("activeSlice")
    if rule["activeSlice"]:
        if not isinstance(active_slice, dict):
            errors.append("activeSlice must be an object")
        else:
            for field in ACTIVE_SLICE_FIELDS:
                require_text(active_slice.get(field), f"activeSlice.{field}", errors)
            backend_platform = active_slice.get("backendPlatform")
            target_root = active_slice.get("targetRoot")
            if isinstance(backend_platform, str) and backend_platform.strip():
                expected_target = BACKEND_TARGETS.get(backend_platform)
                if expected_target is None:
                    errors.append(
                        "activeSlice.backendPlatform must be one of "
                        f"{sorted(BACKEND_TARGETS)}"
                    )
                elif target_root != expected_target:
                    errors.append(
                        "activeSlice.targetRoot must match backendPlatform value "
                        f"{expected_target!r}"
                    )
            if transition in TARGET_TRANSITIONS:
                require_text(
                    active_slice.get("targetRevision"),
                    "activeSlice.targetRevision",
                    errors,
                )

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
        return errors

    try:
        root = repository_root(manifest_path.resolve())
    except ValueError as error:
        errors.append(str(error))
        return errors

    loaded_artifacts: dict[str, dict[str, Any]] = {}
    for field in rule["artifacts"]:
        artifact_path = artifacts.get(field)
        require_text(artifact_path, f"artifacts.{field}", errors)
        if isinstance(artifact_path, str) and artifact_path.strip():
            resolved = (root / artifact_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"artifacts.{field} must stay inside the repository")
                continue
            if not resolved.is_file():
                errors.append(f"artifacts.{field} does not exist: {artifact_path}")
                continue
            if resolved.suffix.lower() == ".json" and field in ARTIFACT_TYPES:
                try:
                    artifact = load_json(resolved)
                except (OSError, json.JSONDecodeError, ValueError) as error:
                    errors.append(f"artifacts.{field} is invalid JSON: {error}")
                    continue
                validate_artifact_identity(artifact, field, manifest, errors)
                loaded_artifacts[field] = artifact
                if field == "discoveryIndex":
                    validate_automated_analysis(artifact, root, errors)
                if field == "slicePlanIndex":
                    validate_data_migration(artifact, root, errors)

    validate_data_gate_artifacts(loaded_artifacts, errors)

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--transition", choices=TRANSITIONS, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_json(args.manifest)
        errors = validate_manifest(manifest, args.manifest, args.transition)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        errors = [str(error)]

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.transition} lifecycle gate is satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
