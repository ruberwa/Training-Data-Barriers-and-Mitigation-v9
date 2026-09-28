from __future__ import annotations

import numpy as np
import pandas as pd

from common.constants import SYNTHETIC_IMAGE_STRATEGIES


def build_analysis_ready(raw: dict[str, pd.DataFrame], analysis_config: dict) -> dict[str, pd.DataFrame]:
    ident = raw["identification"].copy()
    context = raw["context"].copy().rename(columns={"Crop ": "Crop"})
    datasets = raw["datasets"].copy().rename(columns={"Dataset Size": "Dataset Size (images)"})

    master = ident.merge(context, on="Study ID", how="left", validate="one_to_one")
    master = master.merge(datasets, on="Study ID", how="left", validate="one_to_one")
    master["Dataset Size (images)"] = pd.to_numeric(master["Dataset Size (images)"], errors="coerce")
    master["Year"] = pd.to_numeric(master["Year"], errors="coerce").astype("Int64")

    barriers = raw["barriers"].copy().rename(columns={
        "Modules": "Barrier Modules",
        "Barriers": "Normalized Barrier",
    })
    mitigations = raw["mitigations"].copy().rename(columns={"Mitigations": "Mitigation Strategy"})

    key = ["Study ID", "Study Instance ID"]
    mapping = barriers.merge(
        mitigations,
        on=key,
        how="outer",
        validate="one_to_one",
        indicator=True,
    )
    mapping["Barrier-Mitigation Linkage"] = mapping["_merge"].map({
        "both": "Matched",
        "left_only": "Barrier only",
        "right_only": "Mitigation only",
    })
    mapping = mapping.drop(columns="_merge")
    mapping = mapping.merge(master[["Study ID", "Task", "Environment"]], on="Study ID", how="left", validate="many_to_one")
    mapping["Synthetic Image Method"] = mapping["Mitigation Strategy"].isin(SYNTHETIC_IMAGE_STRATEGIES).map({True: "Yes", False: "No"})
    mapping["Synthetic Type"] = mapping["Mitigation Strategy"].where(mapping["Synthetic Image Method"].eq("Yes"), "")

    baselines = raw["baselines"].copy().rename(columns={"Baseline Modules": "Baseline Method"})
    proposed = raw["mitigation_results"].copy().rename(columns={"Mitigation Modules": "Proposed Method"})
    if "Gain" in proposed.columns:
        proposed = proposed.rename(columns={"Gain": "Reported Gain (pp)"})
    else:
        proposed["Reported Gain (pp)"] = pd.NA
    baselines["Baseline (%)"] = pd.to_numeric(baselines["Baseline (%)"], errors="coerce")
    proposed["Mitigation (%)"] = pd.to_numeric(proposed["Mitigation (%)"], errors="coerce")
    proposed["Reported Gain (pp)"] = pd.to_numeric(proposed["Reported Gain (pp)"], errors="coerce")
    proposed = proposed.reset_index(drop=True)
    proposed["Source Result Row"] = np.arange(1, len(proposed) + 1)

    metric_keys = ["Study ID", "Metric", "Metric Family"]
    baseline_match = baselines.rename(columns={"Study Instance ID": "Baseline Study Instance ID"})
    base_cols = metric_keys + ["Baseline Study Instance ID", "Baseline Method", "Baseline (%)"]
    same_instance = proposed.merge(
        baseline_match[base_cols],
        left_on=["Study ID", "Study Instance ID", "Metric", "Metric Family"],
        right_on=["Study ID", "Baseline Study Instance ID", "Metric", "Metric Family"],
        how="left",
    )
    baseline_counts = baselines.groupby(metric_keys)["Baseline (%)"].transform("size")
    single_baseline = baselines.loc[baseline_counts.eq(1)].rename(columns={"Study Instance ID": "Baseline Study Instance ID"})
    study_metric = proposed.merge(single_baseline[base_cols], on=metric_keys, how="left")
    matched_rows = set(same_instance.loc[same_instance["Baseline (%)"].notna(), "Source Result Row"])
    performance = pd.concat(
        [
            same_instance[same_instance["Baseline (%)"].notna()],
            study_metric[~study_metric["Source Result Row"].isin(matched_rows)],
        ],
        ignore_index=True,
    )
    performance = performance[performance["Baseline (%)"].notna()].copy()
    performance["Linkage Status"] = "Matched"
    performance["Calculated Gain (pp)"] = performance["Mitigation (%)"] - performance["Baseline (%)"]
    performance["Gain Difference (reported-calculated)"] = (
        performance["Reported Gain (pp)"] - performance["Calculated Gain (pp)"]
    )

    performance = performance.merge(
        master[["Study ID", "Task", "Environment", "Dataset Size (images)"]],
        on="Study ID", how="left", validate="many_to_one"
    )
    code_cols = key + [
        "Barrier Category", "Normalized Barrier", "Mitigation Category", "Mitigation Strategy",
        "Synthetic Image Method", "Synthetic Type",
    ]
    performance = performance.merge(mapping[code_cols], on=key, how="left", validate="many_to_one")

    primary_metrics = analysis_config["analysis"]["primary_metrics"]
    performance["Primary Metric Eligible"] = [
        "Yes" if str(metric).strip() in set(primary_metrics.get(task, [])) else "No"
        for task, metric in zip(performance["Task"], performance["Metric Family"])
    ]
    performance["Exclusion Reason"] = np.where(
        performance["Primary Metric Eligible"].eq("Yes"), "", "Non-primary task metric"
    )
    performance.insert(0, "Effect ID", [f"V2-E{i:04d}" for i in range(1, len(performance) + 1)])

    audit = proposed.copy()
    linked_rows = set(performance["Source Result Row"].astype(int))
    audit["Linkage Status"] = audit["Source Result Row"].astype(int).map(
        lambda row: "Matched" if row in linked_rows else "No baseline for study and metric"
    )
    study_metric = set(map(tuple, baselines[["Study ID", "Metric", "Metric Family"]].drop_duplicates().values.tolist()))
    audit["Study-metric baseline exists"] = [
        "Yes" if (sid, metric, family) in study_metric else "No"
        for sid, metric, family in zip(audit["Study ID"], audit["Metric"], audit["Metric Family"])
    ]

    quality_raw = raw["quality"].copy()
    quality_columns = {
        "Is the specific training-data barrier(s) clearly identified and described?": "Barrier Clearly Identified",
        "Is the prevalence or severity of the barrier quantified or well justified?": "Barrier Severity Justified",
        "Is the mitigation strategy clearly named and described?": "Mitigation Clearly Described",
        "Is the link between the barrier and the chosen strategy explicitly justified?": "Barrier-Mitigation Link Justified",
        "Are absolute performance values (before and after mitigation) reported with clear metrics?": "Absolute Performance Reported",
        "Is the baseline performance (without the mitigation) clearly reported?": "Baseline Clearly Reported",
        "Is the performance gain calculated and reported transparently?": "Performance Gain Transparent",
        "Are performance results supported by uncertainty/variability evidence such as repeated runs, folds, SD, CI, or multiple seeds?": "Uncertainty Reported",
        "Is the experimental environment clearly stated (field / UAV / greenhouse / lab / controlled)?": "Environment Clearly Stated",
        "Is dataset size (number of images or instances) clearly reported?": "Dataset Size Clearly Reported",
        "Is the computer-vision task clearly specified (Detection / Classification / Segmentation)?": "Task Clearly Specified",
        "Is the evaluation dataset reasonably representative of the intended operating conditions?": "Representative Evaluation",
        "Was a proper independent test set (or external validation) used?": "Independent Test Set",
        "Was data leakage prevented?": "Data Leakage Prevented",
        "Were appropriate metrics used for the task?": "Appropriate Metrics",
        "Are limitations of the training data and mitigation strategy discussed?": "Limitations Discussed",
        "Are training/validation/test samples separated sufficiently to avoid closely related images or acquisition groups appearing across splits?": "Related Samples Separated",
        "If synthetic images were used, is the generation method clearly described?": "Synthetic Generation Described",
        "Is a fair comparison with non-synthetic alternatives provided?": "Fair Non-Synthetic Comparison",
        "Domain-level Concern": "Domain-level Concern",
        "Overall Risk of Bias": "Overall Risk of Bias",
        "Applicability / Generalizability Concern": "Applicability / Generalizability Concern",
    }
    quality = quality_raw.rename(columns=quality_columns)
    quality = quality.merge(master[["Study ID", "Title", "Task"]], on="Study ID", how="left", validate="one_to_one")
    for col in quality_columns.values():
        quality[col] = quality[col].fillna("Not reported").astype(str).str.strip()

    sources = raw["sources"].copy()
    sources = sources.merge(master[["Study ID", "Title"]], on="Study ID", how="left", validate="one_to_one")

    return {
        "study_master": master,
        "barrier_mitigation_map": mapping,
        "performance_results": performance,
        "performance_linkage_audit": audit,
        "evidence_quality": quality,
        "sources": sources,
    }
