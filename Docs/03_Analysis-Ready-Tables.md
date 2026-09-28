**Title:** Build the analysis-ready tables

## What this step does
- Reads `data/Ready Analysis dataset.xlsx`
- Turns the numbered source sheets into the analysis-ready tables
- Leaves the source workbook unchanged
- Writes the tables only after the checks pass

## Run
- From the project root: `python3 src/01_create_analysis_ready_tables.py`

## Link rule
- A barrier is linked to a mitigation on Study ID and Study Instance ID
- A performance comparison uses the baseline for the same Study ID, Metric, and Metric Family
- The baseline is the lower percent. The mitigation is the higher percent. The gain is the higher percent minus the baseline
- When a study has more than one baseline for that metric, the baseline that reproduces the reported gain is used
- A mitigation result stays in the audit only when that study and metric have no baseline
- Synthetic Image Methods covers Data Augmentation and Synthetic Data Generation, and the two subtypes stay separate

## Tables
- **Study Master:** one row per study, with task, environment, year, and dataset size
- **Barrier-Mitigation Map:** which barrier is linked to which mitigation inside each study
- **Performance Results:** baseline versus mitigation for the same study and metric, with the gain calculated as mitigation percent minus baseline percent
- **Performance Linkage Audit:** every mitigation result, including any row whose study and metric have no baseline
- **Evidence Quality:** risk-of-bias and credibility judgments for each study
- **Sources:** source and justification for each study

## Where they are written
- `results/analysis_ready_tables/analysis_ready_tables.xlsx`
  - Study Master
  - Barrier-Mitigation Map
  - Performance Results
  - Performance Linkage Audit
  - Evidence Quality
  - Sources
- `results/analysis_ready_tables/csv/study_master.csv`
- `results/analysis_ready_tables/csv/barrier_mitigation_map.csv`
- `results/analysis_ready_tables/csv/performance_results.csv`
- `results/analysis_ready_tables/csv/performance_linkage_audit.csv`
- `results/analysis_ready_tables/csv/evidence_quality.csv`
- `results/analysis_ready_tables/csv/sources.csv`
- `results/logs/phase1.log`
- `results/validation/phase1_validation.json`

## Check
- Status: PASS
- Study Master and Evidence Quality have one row for each included study
- Each paired mitigation result uses the baseline for the same study and metric
- A mitigation result stays in the audit when that study and metric have no baseline
