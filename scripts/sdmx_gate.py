#!/usr/bin/env python3
"""ENERGIM Alpha SDMX gate.

Validates repository readiness before LEAP/NEMO export. The gate is strict:
candidate crawler evidence is useful, but it does not pass until normalized
data, provenance, transformation logs, and validator quorum are complete.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import shutil
import sys
from typing import Any


REQUIRED_SDMX_DIMENSIONS = {"country", "dataset_id", "scenario", "year", "unit"}
VALID_APPROVALS = {"approved", "approved_with_caveats"}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def repo_path(root: Path, path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    normalized = path_value.replace("\\", "/")
    if normalized.startswith("data/master/"):
        return Path(path_value)
    return root / path


def validation_by_dataset(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["dataset_id"]: row for row in rows if row.get("dataset_id")}


def candidate_count_by_dataset(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        for dataset_id in [part.strip() for part in row.get("matching_alpha_dataset_ids", "").split(";") if part.strip()]:
            counts[dataset_id] = counts.get(dataset_id, 0) + 1
    return counts


def approvals_complete(validation: dict[str, str]) -> tuple[bool, str]:
    aims = validation.get("validator_1_decision", "").strip().lower()
    second = validation.get("validator_2_decision", "").strip().lower()
    third = validation.get("validator_3_decision", "").strip().lower()
    if aims not in VALID_APPROVALS:
        return False, "missing_aims_ric_approval"
    if second not in VALID_APPROVALS or third not in VALID_APPROVALS:
        return False, "missing_two_additional_validator_approvals"
    return True, "validator_quorum_complete"


def gate_dataset(row: dict[str, str], validation: dict[str, str], candidate_count: int, root: Path) -> dict[str, Any]:
    dataset_id = row["dataset_id"]
    checks: list[str] = []
    blockers: list[str] = []

    def require(condition: bool, code: str) -> None:
        checks.append(f"{code}:{'pass' if condition else 'fail'}")
        if not condition:
            blockers.append(code)

    dims = {part.strip() for part in row.get("sdmx_dimensions", "").split(",") if part.strip()}
    normalized_path = repo_path(root, row.get("normalized_dataset_path", ""))
    provenance_path = repo_path(root, row.get("provenance_path", ""))
    transformation_log_path = root / "provenance" / "transformation_logs" / f"{dataset_id}.json"
    dataflow_exists = bool(row.get("sdmx_dataflow_id"))
    transformation_complete = False
    if transformation_log_path.exists():
        try:
            transformation_payload = json.loads(transformation_log_path.read_text(encoding="utf-8"))
            transformation_complete = transformation_payload.get("state") not in {"not_started", "candidate"}
        except json.JSONDecodeError:
            transformation_complete = False

    quorum_ok, quorum_code = approvals_complete(validation)
    unresolved_conflict = validation.get("validation_status", "") == "needs_reconciliation"

    require(bool(dataset_id), "dataset_id_present")
    require(dataflow_exists, "sdmx_dataflow_present")
    require(REQUIRED_SDMX_DIMENSIONS.issubset(dims), "required_dimensions_present")
    require(candidate_count > 0, "candidate_evidence_present")
    require(provenance_path.exists(), "dataset_provenance_present")
    require(transformation_log_path.exists(), "transformation_log_present")
    require(transformation_complete, "transformation_log_complete")
    require(normalized_path.exists(), "normalized_dataset_present")
    require(quorum_ok, quorum_code)
    require(not unresolved_conflict, "no_open_reconciliation")

    status = "pass" if not blockers else "blocked"
    return {
        "dataset_id": dataset_id,
        "dataset_name": row.get("dataset_name", ""),
        "sdmx_dataflow_id": row.get("sdmx_dataflow_id", ""),
        "candidate_evidence_count": candidate_count,
        "validation_status": validation.get("validation_status", "candidate"),
        "normalized_dataset_path": row.get("normalized_dataset_path", ""),
        "provenance_path": row.get("provenance_path", ""),
        "transformation_log_path": str(transformation_log_path).replace("\\", "/"),
        "gate_status": status,
        "blockers": "; ".join(blockers),
        "checks": "; ".join(checks),
    }


def ensure_provenance_files(root: Path, dictionary_rows: list[dict[str, str]], counts: dict[str, int]) -> None:
    for row in dictionary_rows:
        dataset_id = row["dataset_id"]
        provenance_path = repo_path(root, row["provenance_path"])
        transformation_path = root / "provenance" / "transformation_logs" / f"{dataset_id}.json"
        if not provenance_path.exists():
            write_json(
                provenance_path,
                {
                    "dataset_id": dataset_id,
                    "dataset_name": row.get("dataset_name", ""),
                    "state": "candidate",
                    "candidate_evidence_count": counts.get(dataset_id, 0),
                    "source_evidence": "data/master/evidence/evidence_records.jsonl",
                    "candidate_evidence": "data/master/evidence/candidate_evidence.csv",
                    "validation_log": "data/master/validation/validation_log.csv",
                    "sdmx_gate_report": "data/master/sdmx/validation_reports/sdmx_gate_report.csv",
                    "created_by": "scripts/sdmx_gate.py",
                    "updated_utc": utc_now(),
                },
            )
        if not transformation_path.exists():
            write_json(
                transformation_path,
                {
                    "dataset_id": dataset_id,
                    "state": "not_started",
                    "message": "No normalized model data has been transformed yet. Crawler records remain candidate evidence.",
                    "required_before_export": [
                        "source evidence selection",
                        "table or value extraction",
                        "unit normalization",
                        "LEAP/NEMO mapping confirmation",
                        "validator quorum",
                    ],
                    "updated_utc": utc_now(),
                },
            )


def run_gate(root: Path) -> dict[str, Any]:
    dictionary_path = root / "catalog" / "dataset_dictionary.csv"
    validation_path = root / "validation" / "validation_log.csv"
    evidence_path = root / "evidence" / "candidate_evidence.csv"
    report_path = root / "sdmx" / "validation_reports" / "sdmx_gate_report.csv"
    report_json_path = root / "sdmx" / "validation_reports" / "sdmx_gate_report.json"

    dictionary_rows = read_csv(dictionary_path)
    validation_rows = validation_by_dataset(read_csv(validation_path))
    evidence_counts = candidate_count_by_dataset(read_csv(evidence_path))
    ensure_provenance_files(root, dictionary_rows, evidence_counts)

    report_rows = []
    for row in dictionary_rows:
        validation = validation_rows.get(row["dataset_id"], {})
        report_rows.append(gate_dataset(row, validation, evidence_counts.get(row["dataset_id"], 0), root))

    fields = [
        "dataset_id",
        "dataset_name",
        "sdmx_dataflow_id",
        "candidate_evidence_count",
        "validation_status",
        "normalized_dataset_path",
        "provenance_path",
        "transformation_log_path",
        "gate_status",
        "blockers",
        "checks",
    ]
    write_csv(report_path, report_rows, fields)

    payload = {
        "gate": "ENERGIM Alpha SDMX Gate",
        "run_utc": utc_now(),
        "dataset_count": len(report_rows),
        "passed_count": sum(1 for row in report_rows if row["gate_status"] == "pass"),
        "blocked_count": sum(1 for row in report_rows if row["gate_status"] != "pass"),
        "report_csv": str(report_path).replace("\\", "/"),
        "rule": "No LEAP/NEMO export until SDMX gate passes and validator quorum is complete.",
    }
    write_json(report_json_path, payload)

    copy_if_exists(root / "catalog" / "data_catalog.csv", root / "exports" / "csv" / "master_catalog_export.csv")
    copy_if_exists(root / "evidence" / "candidate_evidence.csv", root / "exports" / "csv" / "candidate_evidence_export.csv")
    copy_if_exists(report_path, root / "exports" / "sdmx" / "sdmx_gate_report.csv")
    copy_if_exists(root / "sdmx" / "dsd" / "energim_alpha_dsd.json", root / "exports" / "sdmx" / "energim_alpha_dsd.json")
    copy_if_exists(root / "sdmx" / "dataflows" / "dataflows.csv", root / "exports" / "sdmx" / "dataflows.csv")

    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ENERGIM Alpha SDMX gate")
    parser.add_argument("--root", default="data/master", help="Master repository root")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    payload = run_gate(Path(args.root))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
