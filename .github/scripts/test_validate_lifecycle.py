from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_lifecycle import (
    validate_automated_analysis,
    validate_data_gate_artifacts,
    validate_manifest,
)


class ValidateLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / ".github").mkdir()
        (self.root / "modernization" / "APP-TEST" / "analysis").mkdir(parents=True)
        self.discovery_index = (
            self.root
            / "modernization"
            / "APP-TEST"
            / "analysis"
            / "discovery-index.json"
        )
        self.discovery_index.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "artifactType": "discovery-index",
                    "applicationId": "APP-TEST",
                    "sourceRevision": "source-1",
                }
            ),
            encoding="utf-8",
        )
        self.manifest_path = self.root / "modernization" / "APP-TEST" / "lifecycle.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def manifest(self) -> dict[str, object]:
        return {
            "schemaVersion": 1,
            "applicationId": "APP-TEST",
            "sourceRevision": "source-1",
            "currentStage": "discovery",
            "status": "approved",
            "activeSlice": None,
            "artifacts": {
                "discoveryIndex": (
                    "modernization/APP-TEST/analysis/discovery-index.json"
                )
            },
            "approval": {
                "decision": "approved",
                "approvedBy": "reviewer",
                "approvedAt": "2026-08-18T00:00:00Z",
                "decisionReference": "review-1",
            },
            "criticalGaps": [],
        }

    def data_migration_artifacts(self) -> dict[str, dict[str, object]]:
        return {
            "slicePlanIndex": {
                "dataMigration": {
                    "inScope": True,
                    "sourceSnapshotReference": "snapshot-1",
                    "reconciliation": {"rejectedRowTolerance": 0},
                }
            }
        }

    def test_approved_discovery_can_transition_to_planning(self) -> None:
        errors = validate_manifest(self.manifest(), self.manifest_path, "to-planning")
        self.assertEqual([], errors)

    def test_pending_approval_blocks_transition(self) -> None:
        manifest = self.manifest()
        manifest["approval"]["decision"] = "pending"
        errors = validate_manifest(manifest, self.manifest_path, "to-planning")
        self.assertIn("approval.decision must be 'approved'", errors)

    def test_critical_gap_blocks_transition(self) -> None:
        manifest = self.manifest()
        manifest["criticalGaps"] = [{"gapId": "GAP-TEST-001"}]
        errors = validate_manifest(manifest, self.manifest_path, "to-planning")
        self.assertIn(
            "criticalGaps must be empty before a lifecycle transition", errors
        )

    def test_missing_artifact_blocks_transition(self) -> None:
        self.discovery_index.unlink()
        errors = validate_manifest(self.manifest(), self.manifest_path, "to-planning")
        self.assertTrue(any("does not exist" in error for error in errors))

    def test_mismatched_artifact_revision_blocks_transition(self) -> None:
        artifact = json.loads(self.discovery_index.read_text(encoding="utf-8"))
        artifact["sourceRevision"] = "different-source"
        self.discovery_index.write_text(json.dumps(artifact), encoding="utf-8")
        errors = validate_manifest(self.manifest(), self.manifest_path, "to-planning")
        self.assertTrue(any("sourceRevision must match" in error for error in errors))

    def test_automated_analysis_requires_candidate_evidence_and_reconciliation(
        self,
    ) -> None:
        analysis_directory = (
            self.root / "modernization" / "APP-TEST" / "evidence" / "automated-analysis"
        )
        analysis_directory.mkdir(parents=True)
        analysis_path = analysis_directory / "analysis.json"
        analysis_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "artifactType": "automated-cobol-analysis",
                    "applicationId": "APP-TEST",
                    "sourceRevision": "source-1",
                    "analyzer": {"capability": "authoritative"},
                    "coverage": {
                        "attempted": 1,
                        "succeeded": 0,
                        "partial": 0,
                        "failed": 1,
                        "errorCount": 1,
                    },
                    "limitations": [],
                    "files": [{}],
                }
            ),
            encoding="utf-8",
        )
        discovery = {
            "applicationId": "APP-TEST",
            "sourceRevision": "source-1",
            "automatedAnalysis": {
                "inScope": True,
                "artifactPath": analysis_path.relative_to(self.root).as_posix(),
                "reconciliationPath": "modernization/APP-TEST/missing.md",
            },
        }

        errors: list[str] = []
        validate_automated_analysis(discovery, self.root, errors)

        self.assertTrue(
            any("reconciliationPath does not exist" in item for item in errors)
        )
        self.assertTrue(any("candidate-evidence-only" in item for item in errors))
        self.assertTrue(any("coverage.failed must be 0" in item for item in errors))
        self.assertTrue(
            any("limitations must be a non-empty array" in item for item in errors)
        )

    def test_reconciled_automated_analysis_is_accepted(self) -> None:
        analysis_directory = (
            self.root / "modernization" / "APP-TEST" / "evidence" / "automated-analysis"
        )
        analysis_directory.mkdir(parents=True)
        analysis_path = analysis_directory / "analysis.json"
        reconciliation_path = analysis_directory / "reconciliation.md"
        reconciliation_path.write_text("Reviewed candidate evidence", encoding="utf-8")
        analysis_path.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "artifactType": "automated-cobol-analysis",
                    "applicationId": "APP-TEST",
                    "sourceRevision": "source-1",
                    "analyzer": {"capability": "candidate-evidence-only"},
                    "coverage": {
                        "attempted": 1,
                        "succeeded": 0,
                        "partial": 1,
                        "failed": 0,
                        "errorCount": 0,
                    },
                    "limitations": ["Not a runtime oracle"],
                    "files": [{"status": "partial"}],
                }
            ),
            encoding="utf-8",
        )
        discovery = {
            "applicationId": "APP-TEST",
            "sourceRevision": "source-1",
            "automatedAnalysis": {
                "inScope": True,
                "artifactPath": analysis_path.relative_to(self.root).as_posix(),
                "reconciliationPath": reconciliation_path.relative_to(
                    self.root
                ).as_posix(),
            },
        }

        errors: list[str] = []
        validate_automated_analysis(discovery, self.root, errors)

        self.assertEqual([], errors)

    def test_validation_transition_requires_target_revision(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "implementation"
        manifest["status"] = "implemented"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "java-spring",
            "targetRoot": "target/react-spring-azure-sql",
        }
        artifacts = manifest["artifacts"]
        for field in (
            "slicePlanIndex",
            "traceabilityIndex",
            "implementationReport",
        ):
            path = self.root / "modernization" / "APP-TEST" / f"{field}.json"
            path.write_text("{}", encoding="utf-8")
            artifacts[field] = path.relative_to(self.root).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-validation")
        self.assertIn("activeSlice.targetRevision must be a non-empty string", errors)

    def test_deployment_apply_requires_human_approval(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "deployment"
        manifest["status"] = "planned"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "java-spring",
            "targetRoot": "target/react-spring-azure-sql",
            "targetRevision": "target-1",
        }
        manifest["approval"]["decision"] = "pending"
        deployment_plan = self.root / "modernization" / "APP-TEST" / "plan.json"
        deployment_plan.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "artifactType": "deployment-plan",
                    "applicationId": "APP-TEST",
                    "sourceRevision": "source-1",
                    "sliceId": "SLICE-TEST-001",
                    "planRevision": "1",
                    "contractRevision": "1",
                    "oracleSetRevision": "1",
                    "backendPlatform": "java-spring",
                    "targetRoot": "target/react-spring-azure-sql",
                    "targetRevision": "target-1",
                }
            ),
            encoding="utf-8",
        )
        manifest["artifacts"]["deploymentPlan"] = deployment_plan.relative_to(
            self.root
        ).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-deployment-apply")

        self.assertIn("approval.decision must be 'approved'", errors)

    def test_azure_validation_requires_revision_bound_deployment_report(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "deployment"
        manifest["status"] = "deployed"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "java-spring",
            "targetRoot": "target/react-spring-azure-sql",
            "targetRevision": "target-1",
        }
        for field, artifact_type in (
            ("deploymentPlan", "deployment-plan"),
            ("deploymentReport", "deployment-report"),
        ):
            path = self.root / "modernization" / "APP-TEST" / f"{field}.json"
            path.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "artifactType": artifact_type,
                        "applicationId": "APP-TEST",
                        "sourceRevision": "source-1",
                        "sliceId": "SLICE-TEST-001",
                        "planRevision": "1",
                        "contractRevision": "1",
                        "oracleSetRevision": "1",
                        "backendPlatform": "java-spring",
                        "targetRoot": "target/react-spring-azure-sql",
                        "targetRevision": "different-target",
                    }
                ),
                encoding="utf-8",
            )
            manifest["artifacts"][field] = path.relative_to(self.root).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-azure-validation")

        self.assertTrue(any("targetRevision must match" in error for error in errors))

    def test_implementation_rejects_backend_target_mismatch(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "planning"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "dotnet-aspnet-core",
            "targetRoot": "target/react-spring-azure-sql",
        }
        artifacts = manifest["artifacts"]
        for field in ("slicePlanIndex", "traceabilityIndex"):
            path = self.root / "modernization" / "APP-TEST" / f"{field}.json"
            path.write_text("{}", encoding="utf-8")
            artifacts[field] = path.relative_to(self.root).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-implementation")

        self.assertIn(
            "activeSlice.targetRoot must match backendPlatform value "
            "'target/react-dotnet-azure-sql'",
            errors,
        )

    def test_approved_dotnet_slice_can_transition_to_implementation(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "planning"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "dotnet-aspnet-core",
            "targetRoot": "target/react-dotnet-azure-sql",
        }
        artifacts = manifest["artifacts"]
        artifact_types = {
            "slicePlanIndex": "slice-plan-index",
            "traceabilityIndex": "traceability-index",
        }
        data_paths = {}
        for field, name in (
            ("sourceToTargetMapPath", "source-to-target-map.csv"),
            ("dataProfilePath", "data-profile.md"),
            ("migrationRunbookPath", "migration-runbook.md"),
            ("reconciliationPlanPath", "reconciliation-plan.md"),
            ("recoveryRunbookPath", "recovery-runbook.md"),
        ):
            path = self.root / "modernization" / "APP-TEST" / name
            path.write_text("test evidence", encoding="utf-8")
            data_paths[field] = path.relative_to(self.root).as_posix()
        for field, artifact_type in artifact_types.items():
            path = self.root / "modernization" / "APP-TEST" / f"{field}.json"
            data_migration = {}
            if field == "slicePlanIndex":
                data_migration = {
                    "dataMigration": {
                        "inScope": True,
                        "sourceSnapshotReference": "snapshot-1",
                        **data_paths,
                        "reconciliation": {
                            "rowCountTolerance": 0,
                            "rejectedRowTolerance": 0,
                            "controlTotalTolerance": "0.00",
                            "hashMethod": "SHA-256 over canonicalized fields",
                        },
                        "recoveryMode": "forward-recovery",
                    }
                }
            path.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "artifactType": artifact_type,
                        "applicationId": "APP-TEST",
                        "sourceRevision": "source-1",
                        **manifest["activeSlice"],
                        **data_migration,
                    }
                ),
                encoding="utf-8",
            )
            artifacts[field] = path.relative_to(self.root).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-implementation")

        self.assertEqual([], errors)

    def test_implementation_requires_data_migration_controls(self) -> None:
        manifest = self.manifest()
        manifest["currentStage"] = "planning"
        manifest["activeSlice"] = {
            "sliceId": "SLICE-TEST-001",
            "planRevision": "1",
            "contractRevision": "1",
            "oracleSetRevision": "1",
            "backendPlatform": "java-spring",
            "targetRoot": "target/react-spring-azure-sql",
        }
        artifacts = manifest["artifacts"]
        for field, artifact_type in (
            ("slicePlanIndex", "slice-plan-index"),
            ("traceabilityIndex", "traceability-index"),
        ):
            path = self.root / "modernization" / "APP-TEST" / f"{field}.json"
            path.write_text(
                json.dumps(
                    {
                        "schemaVersion": 1,
                        "artifactType": artifact_type,
                        "applicationId": "APP-TEST",
                        "sourceRevision": "source-1",
                        **manifest["activeSlice"],
                    }
                ),
                encoding="utf-8",
            )
            artifacts[field] = path.relative_to(self.root).as_posix()

        errors = validate_manifest(manifest, self.manifest_path, "to-implementation")

        self.assertIn(
            "artifacts.slicePlanIndex dataMigration must be an object", errors
        )

    def test_validation_requires_passed_data_migration_evidence(self) -> None:
        artifacts = self.data_migration_artifacts()
        artifacts["validationGateReport"] = {"dataMigrationEvidence": {}}

        errors: list[str] = []
        validate_data_gate_artifacts(artifacts, errors)

        self.assertIn(
            "artifacts.validationGateReport dataMigrationEvidence."
            "dataReconciliationResult must be 'passed'",
            errors,
        )
        self.assertIn(
            "artifacts.validationGateReport dataMigrationEvidence."
            "recoveryRehearsalResult must be 'passed'",
            errors,
        )

    def test_deployment_plan_requires_database_recovery_evidence(self) -> None:
        artifacts = self.data_migration_artifacts()
        artifacts["deploymentPlan"] = {"databaseChange": {}}

        errors: list[str] = []
        validate_data_gate_artifacts(artifacts, errors)

        self.assertIn(
            "artifacts.deploymentPlan databaseChange."
            "preMigrationBackupReference must be a non-empty string",
            errors,
        )
        self.assertIn(
            "artifacts.deploymentPlan databaseChange."
            "restoreRehearsalReference must be a non-empty string",
            errors,
        )

    def test_deployment_report_enforces_snapshot_and_reject_tolerance(self) -> None:
        artifacts = self.data_migration_artifacts()
        artifacts["deploymentPlan"] = {
            "databaseChange": {"sourceSnapshotReference": "snapshot-1"}
        }
        artifacts["deploymentReport"] = {
            "dataReconciliation": {
                "sourceSnapshotReference": "snapshot-2",
                "rowCountResult": "passed",
                "controlTotalResult": "passed",
                "hashResult": "passed",
                "rejectedRowCount": 1,
                "exceptionReferences": [],
            }
        }

        errors: list[str] = []
        validate_data_gate_artifacts(artifacts, errors)

        self.assertIn(
            "artifacts.deploymentReport dataReconciliation."
            "rejectedRowCount exceeds approved tolerance 0",
            errors,
        )
        self.assertIn(
            "artifacts.deploymentReport dataReconciliation."
            "sourceSnapshotReference must match deployment plan",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
