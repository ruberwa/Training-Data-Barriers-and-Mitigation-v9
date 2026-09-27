from __future__ import annotations

import pandas as pd

from common.Messages import (
    no_exact_comparisons,
    quality_duplicate,
    study_master_duplicate,
    study_master_row_mismatch,
)


def duplicate_key_count(frame: pd.DataFrame, cols: list[str]) -> int:
    if not set(cols).issubset(frame.columns):
        return -1
    return int(frame.duplicated(cols).sum())


def phase1_validation(raw: dict[str, pd.DataFrame], ready: dict[str, pd.DataFrame]) -> dict:
    master = ready["study_master"]
    perf = ready["performance_results"]
    audit = ready["performance_linkage_audit"]
    mapping = ready["barrier_mitigation_map"]
    quality = ready["evidence_quality"]
    checks = {
        "raw_identification_rows": int(len(raw["identification"])),
        "unique_studies": int(master["Study ID"].nunique()),
        "study_master_rows": int(len(master)),
        "barrier_rows": int(len(raw["barriers"])),
        "mitigation_rows": int(len(raw["mitigations"])),
        "barrier_mitigation_rows": int(len(mapping)),
        "baseline_rows": int(len(raw["baselines"])),
        "mitigation_result_rows": int(len(raw["mitigation_results"])),
        "exact_linked_performance_rows": int(len(perf)),
        "unlinked_mitigation_result_rows": int((audit["Linkage Status"] != "Exact match").sum()),
        "quality_rows": int(len(quality)),
        "duplicate_study_ids_master": duplicate_key_count(master, ["Study ID"]),
        "duplicate_quality_study_ids": duplicate_key_count(quality, ["Study ID"]),
    }
    failures = []
    if checks["unique_studies"] != checks["raw_identification_rows"]:
        failures.append(study_master_row_mismatch())
    if checks["duplicate_study_ids_master"] != 0:
        failures.append(study_master_duplicate())
    if checks["duplicate_quality_study_ids"] != 0:
        failures.append(quality_duplicate())
    if checks["exact_linked_performance_rows"] == 0:
        failures.append(no_exact_comparisons())
    return {
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failures": failures,
    }
