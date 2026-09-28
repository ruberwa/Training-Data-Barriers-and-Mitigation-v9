from __future__ import annotations

import pandas as pd

from common.constants import STATUS_ELIGIBLE, STATUS_INELIGIBLE, STATUS_PENDING
from common.Messages import (
    audit_count_mismatch,
    gain_mismatch,
    pending_remain,
    performance_not_eligible,
    profile_count_mismatch,
    quality_duplicate,
    quality_row_mismatch,
    register_count_mismatch,
    register_duplicate,
    register_status_unknown,
    selected_result_reused,
    study_master_duplicate,
    study_master_row_mismatch,
)

KNOWN_STATUSES = {STATUS_ELIGIBLE, STATUS_INELIGIBLE, STATUS_PENDING}
REGISTER_KEY = ["Study ID", "Baseline Study Instance ID"]


def duplicate_key_count(frame: pd.DataFrame, cols: list[str]) -> int:
    if not set(cols).issubset(frame.columns):
        return -1
    return int(frame.duplicated(cols).sum())


def phase1_validation(raw: dict[str, pd.DataFrame], ready: dict[str, pd.DataFrame]) -> dict:
    master = ready["study_master"]
    register = ready["comparison_register"]
    performance = ready["performance_results"]
    audit = ready["performance_linkage_audit"]
    quality = ready["evidence_quality"]
    eligible = register[register["Status"].eq(STATUS_ELIGIBLE)]
    signed = pd.to_numeric(eligible["Signed Gain (pp)"], errors="coerce")
    calculated = pd.to_numeric(eligible["Mitigation (%)"], errors="coerce") - pd.to_numeric(eligible["Baseline (%)"], errors="coerce")
    gain_gaps = int((signed - calculated).abs().gt(1e-6).fillna(True).sum())
    withheld = register[register["Status"].ne(STATUS_ELIGIBLE)]
    if withheld["Signed Gain (pp)"].notna().any():
        gain_gaps += int(withheld["Signed Gain (pp)"].notna().sum())
    checks = {
        "raw_identification_rows": int(len(raw["identification"])),
        "unique_studies": int(master["Study ID"].nunique()),
        "study_master_rows": int(len(master)),
        "barrier_rows": int(len(raw["barriers"])),
        "mitigation_rows": int(len(raw["mitigations"])),
        "barrier_profile_rows": int(len(ready["barrier_profile"])),
        "mitigation_profile_rows": int(len(ready["mitigation_profile"])),
        "cooccurrence_rows": int(len(ready["barrier_mitigation_cooccurrence"])),
        "baseline_rows": int(len(raw["baselines"])),
        "register_rows": int(len(register)),
        "eligible_rows": int(register["Status"].eq(STATUS_ELIGIBLE).sum()),
        "ineligible_rows": int(register["Status"].eq(STATUS_INELIGIBLE).sum()),
        "pending_rows": int(register["Status"].eq(STATUS_PENDING).sum()),
        "mitigation_result_rows": int(len(raw["mitigation_results"])),
        "audit_rows": int(len(audit)),
        "performance_rows": int(len(performance)),
        "quality_rows": int(len(quality)),
        "duplicate_study_ids_master": duplicate_key_count(master, ["Study ID"]),
        "duplicate_quality_study_ids": duplicate_key_count(quality, ["Study ID"]),
        "duplicate_baseline_contexts": duplicate_key_count(register, REGISTER_KEY),
        "gain_mismatches": gain_gaps,
    }
    failures = []
    if checks["study_master_rows"] != checks["raw_identification_rows"] or checks["unique_studies"] != checks["raw_identification_rows"]:
        failures.append(study_master_row_mismatch())
    if checks["duplicate_study_ids_master"] != 0:
        failures.append(study_master_duplicate())
    if checks["quality_rows"] != checks["raw_identification_rows"]:
        failures.append(quality_row_mismatch())
    if checks["duplicate_quality_study_ids"] != 0:
        failures.append(quality_duplicate())
    if checks["barrier_profile_rows"] != checks["barrier_rows"] or checks["mitigation_profile_rows"] != checks["mitigation_rows"]:
        failures.append(profile_count_mismatch())
    if checks["register_rows"] != checks["baseline_rows"]:
        failures.append(register_count_mismatch())
    if checks["duplicate_baseline_contexts"] != 0:
        failures.append(register_duplicate())
    if checks["pending_rows"] != 0:
        failures.append(pending_remain())
    if checks["gain_mismatches"] != 0:
        failures.append(gain_mismatch())
    if checks["audit_rows"] != checks["mitigation_result_rows"]:
        failures.append(audit_count_mismatch())
    if not set(register["Status"]).issubset(KNOWN_STATUSES):
        failures.append(register_status_unknown())
    if register.loc[register["Status"].eq(STATUS_ELIGIBLE), "Selected Source Result Row"].dropna().duplicated().any():
        failures.append(selected_result_reused())
    if set(performance["Comparison ID"]) != set(eligible["Comparison ID"]):
        failures.append(performance_not_eligible())
    return {
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failures": failures,
    }
