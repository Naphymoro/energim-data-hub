#!/usr/bin/env python3
"""Build visible LEAP/NEMO model input queues from crawler evidence.

The crawler finds candidate evidence. This script makes the next layer visible:
which candidate records could feed each LEAP or NEMO input, what normalized file
must be created, and why the item is still blocked or ready.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import shutil
from typing import Any


CONFIDENCE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


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


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def evidence_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    tier_raw = row.get("source_tier", "").strip()
    try:
        tier = int(tier_raw)
    except ValueError:
        tier = 99
    confidence = CONFIDENCE_ORDER.get(row.get("confidence_level", "").strip().upper(), 99)
    return (tier, confidence, row.get("institution", ""))


def build_evidence_index(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_dataset: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        for dataset_id in split_semicolon(row.get("matching_alpha_dataset_ids", "")):
            by_dataset.setdefault(dataset_id, []).append(row)
    for dataset_rows in by_dataset.values():
        dataset_rows.sort(key=evidence_sort_key)
    return by_dataset


def by_dataset(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["dataset_id"]: row for row in rows if row.get("dataset_id")}


def unique_join(values: list[str], limit: int = 5) -> str:
    seen: list[str] = []
    for value in values:
        clean = value.strip()
        if clean and clean not in seen:
            seen.append(clean)
    if len(seen) > limit:
        return "; ".join(seen[:limit]) + f"; +{len(seen) - limit} more"
    return "; ".join(seen)


def release_state(gate_status: str, validation_status: str, evidence_count: int) -> str:
    if gate_status == "passed" and validation_status in {"validated", "approved"}:
        return "ready_for_export"
    if evidence_count == 0:
        return "needs_crawler_evidence"
    return "candidate_evidence_pending_extraction"


def next_action(state: str, blockers: str) -> str:
    if state == "ready_for_export":
        return "Export to LEAP/NEMO and archive release snapshot."
    if state == "needs_crawler_evidence":
        return "Run crawler again or manually add official source evidence for this dataset."
    if "normalized_dataset_present" in blockers:
        return "Extract numeric values from candidate evidence and create the normalized CSV at the listed path."
    if "missing_aims_ric_approval" in blockers:
        return "Send normalized dataset to AIMS RIC and two approved validators."
    if "transformation_log_complete" in blockers:
        return "Complete the transformation log after extraction and normalization."
    return "Resolve SDMX gate blockers and validator comments."


def queue_row(
    dataset: dict[str, str],
    gate: dict[str, str],
    evidence_rows: list[dict[str, str]],
    model: str,
) -> dict[str, Any]:
    validation_status = gate.get("validation_status", dataset.get("export_ready", "candidate"))
    gate_status = gate.get("gate_status", "not_run")
    blockers = gate.get("blockers", "")
    state = release_state(gate_status, validation_status, len(evidence_rows))
    top = evidence_rows[:5]
    return {
        "dataset_id": dataset.get("dataset_id", ""),
        "dataset_name": dataset.get("dataset_name", ""),
        "model": model,
        "leap_module": dataset.get("leap_module", ""),
        "leap_branch": dataset.get("leap_branch", ""),
        "leap_variable": dataset.get("leap_variable", ""),
        "leap_unit": dataset.get("leap_unit", ""),
        "nemo_component": dataset.get("nemo_component", ""),
        "nemo_mapping": dataset.get("nemo_mapping", ""),
        "sdmx_dataflow_id": dataset.get("sdmx_dataflow_id", ""),
        "required_grain": dataset.get("required_grain", ""),
        "normalized_dataset_path": dataset.get("normalized_dataset_path", ""),
        "candidate_evidence_count": len(evidence_rows),
        "top_evidence_ids": unique_join([row.get("evidence_id", "") for row in top]),
        "top_institutions": unique_join([row.get("institution", "") for row in top]),
        "top_source_urls": unique_join([row.get("discovered_url", "") for row in top], limit=3),
        "detected_years": unique_join([row.get("years_detected", "") for row in evidence_rows]),
        "detected_units": unique_join([row.get("units_detected", "") for row in evidence_rows]),
        "validation_status": validation_status,
        "sdmx_gate_status": gate_status,
        "release_state": state,
        "blockers": blockers,
        "next_action": next_action(state, blockers),
    }


def build_crosswalk(
    datasets: list[dict[str, str]],
    evidence_index: dict[str, list[dict[str, str]]],
) -> list[dict[str, Any]]:
    datasets_by_id = {row.get("dataset_id", ""): row for row in datasets}
    rows: list[dict[str, Any]] = []
    for dataset_id, evidence_rows in sorted(evidence_index.items()):
        dataset = datasets_by_id.get(dataset_id, {})
        for evidence in evidence_rows:
            rows.append(
                {
                    "dataset_id": dataset_id,
                    "dataset_name": dataset.get("dataset_name", ""),
                    "evidence_id": evidence.get("evidence_id", ""),
                    "source_id": evidence.get("source_id", ""),
                    "institution": evidence.get("institution", ""),
                    "source_tier": evidence.get("source_tier", ""),
                    "title": evidence.get("title", ""),
                    "discovered_url": evidence.get("discovered_url", ""),
                    "file_type": evidence.get("file_type", ""),
                    "leap_module": dataset.get("leap_module", ""),
                    "leap_branch": dataset.get("leap_branch", ""),
                    "leap_variable": dataset.get("leap_variable", ""),
                    "nemo_component": dataset.get("nemo_component", ""),
                    "nemo_mapping": dataset.get("nemo_mapping", ""),
                    "years_detected": evidence.get("years_detected", ""),
                    "units_detected": evidence.get("units_detected", ""),
                    "confidence_level": evidence.get("confidence_level", ""),
                    "validation_status": evidence.get("validation_status", ""),
                }
            )
    rows.sort(key=lambda row: (row["dataset_id"], row["source_tier"], row["institution"], row["evidence_id"]))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build LEAP/NEMO model input queues from ENERGIM crawler evidence.")
    parser.add_argument("--root", default="data/master", help="Master data repository root.")
    args = parser.parse_args()

    root = Path(args.root)
    datasets = read_csv(root / "catalog" / "dataset_dictionary.csv")
    evidence_rows = read_csv(root / "evidence" / "candidate_evidence.csv")
    gate_rows = by_dataset(read_csv(root / "sdmx" / "validation_reports" / "sdmx_gate_report.csv"))
    evidence_index = build_evidence_index(evidence_rows)

    all_rows = [queue_row(dataset, gate_rows.get(dataset.get("dataset_id", ""), {}), evidence_index.get(dataset.get("dataset_id", ""), []), "LEAP/NEMO") for dataset in datasets]
    leap_rows = [
        queue_row(dataset, gate_rows.get(dataset.get("dataset_id", ""), {}), evidence_index.get(dataset.get("dataset_id", ""), []), "LEAP")
        for dataset in datasets
        if dataset.get("leap_module")
    ]
    nemo_rows = [
        queue_row(dataset, gate_rows.get(dataset.get("dataset_id", ""), {}), evidence_index.get(dataset.get("dataset_id", ""), []), "NEMO")
        for dataset in datasets
        if dataset.get("nemo_component")
    ]
    crosswalk_rows = build_crosswalk(datasets, evidence_index)

    queue_fields = [
        "dataset_id",
        "dataset_name",
        "model",
        "leap_module",
        "leap_branch",
        "leap_variable",
        "leap_unit",
        "nemo_component",
        "nemo_mapping",
        "sdmx_dataflow_id",
        "required_grain",
        "normalized_dataset_path",
        "candidate_evidence_count",
        "top_evidence_ids",
        "top_institutions",
        "top_source_urls",
        "detected_years",
        "detected_units",
        "validation_status",
        "sdmx_gate_status",
        "release_state",
        "blockers",
        "next_action",
    ]
    crosswalk_fields = [
        "dataset_id",
        "dataset_name",
        "evidence_id",
        "source_id",
        "institution",
        "source_tier",
        "title",
        "discovered_url",
        "file_type",
        "leap_module",
        "leap_branch",
        "leap_variable",
        "nemo_component",
        "nemo_mapping",
        "years_detected",
        "units_detected",
        "confidence_level",
        "validation_status",
    ]

    model_input_dir = root / "model_inputs"
    write_csv(model_input_dir / "model_input_queue.csv", all_rows, queue_fields)
    write_csv(model_input_dir / "leap_model_input_queue.csv", leap_rows, queue_fields)
    write_csv(model_input_dir / "nemo_model_input_queue.csv", nemo_rows, queue_fields)
    write_csv(model_input_dir / "evidence_to_model_input_crosswalk.csv", crosswalk_rows, crosswalk_fields)

    copy_file(model_input_dir / "leap_model_input_queue.csv", root / "normalized" / "leap" / "model_input_queue.csv")
    copy_file(model_input_dir / "nemo_model_input_queue.csv", root / "normalized" / "nemo" / "model_input_queue.csv")
    copy_file(model_input_dir / "model_input_queue.csv", root / "exports" / "csv" / "model_input_queue.csv")
    copy_file(model_input_dir / "leap_model_input_queue.csv", root / "exports" / "csv" / "leap_model_input_queue.csv")
    copy_file(model_input_dir / "nemo_model_input_queue.csv", root / "exports" / "csv" / "nemo_model_input_queue.csv")
    copy_file(model_input_dir / "evidence_to_model_input_crosswalk.csv", root / "exports" / "csv" / "evidence_to_model_input_crosswalk.csv")

    summary = {
        "generated_at_utc": utc_now(),
        "dataset_count": len(datasets),
        "candidate_evidence_count": len(evidence_rows),
        "evidence_to_model_mapping_count": len(crosswalk_rows),
        "leap_input_count": len(leap_rows),
        "nemo_input_count": len(nemo_rows),
        "ready_for_export_count": sum(1 for row in all_rows if row.get("release_state") == "ready_for_export"),
        "blocked_or_pending_count": sum(1 for row in all_rows if row.get("release_state") != "ready_for_export"),
    }
    write_json(model_input_dir / "model_input_summary.json", summary)

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
