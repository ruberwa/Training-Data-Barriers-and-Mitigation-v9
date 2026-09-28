ANALYSIS_READY_FILES = {
    "study_master": "study_master.csv",
    "barrier_profile": "barrier_profile.csv",
    "mitigation_profile": "mitigation_profile.csv",
    "barrier_mitigation_cooccurrence": "barrier_mitigation_cooccurrence.csv",
    "comparison_register": "comparison_register.csv",
    "performance_results": "performance_results.csv",
    "performance_linkage_audit": "performance_linkage_audit.csv",
    "evidence_quality": "evidence_quality.csv",
    "sources": "sources.csv",
}

ANALYSIS_READY_SHEETS = {
    "study_master": "Study Master",
    "barrier_profile": "Barrier Profile",
    "mitigation_profile": "Mitigation Profile",
    "barrier_mitigation_cooccurrence": "Co-occurrence",
    "comparison_register": "Comparison Register",
    "performance_results": "Performance Results",
    "performance_linkage_audit": "Performance Linkage Audit",
    "evidence_quality": "Evidence Quality",
    "sources": "Sources",
}

STATUS_ELIGIBLE = "Eligible"
STATUS_INELIGIBLE = "Ineligible"
STATUS_PENDING = "Pending"

SYNTHETIC_IMAGE_STRATEGIES = {"Data Augmentation", "Synthetic Data Generation"}

RAW_SHEETS = {
    "identification": ("1-Study Identification", 1),
    "context": ("2-Application Context", 1),
    "datasets": ("4-Dataset Characteristics", 1),
    "barriers": ("5-Barrier Coding", 2),
    "mitigations": ("6-Mitigation Strategy Coding", 2),
    "baselines": ("7-Baseline Performance Results", 2),
    "mitigation_results": ("8-Mitigation Performance Result", 2),
    "quality": ("9-Quality & Risk of Bias", 1),
    "sources": ("10-Source & Justification", 2),
}
