**Title:** Build the analysis-ready tables

## What this step does
- Reads `data/Analysis-ready-dataset.xlsx`
- Turns the nine source sheets into six tables
- Leaves the source workbook unchanged
- Writes the tables only after the checks pass

## Run
- From the project root: `python3 src/01_create_analysis_ready_tables.py`

## Link rule
- A barrier is linked to a mitigation on Study ID and Study Instance ID
- A performance comparison is kept only when Study ID, Study Instance ID, Metric, and Metric Family all match
- Mitigation results with no exact baseline stay in the audit
- Synthetic Image Methods covers Data Augmentation and Synthetic Data Generation, and the two subtypes stay separate

## Tables
- **Study Master:** one row per study, with task, environment, year, and dataset size. 154 rows
- **Barrier-Mitigation Map:** which barrier is linked to which mitigation inside each study. 544 rows
- **Performance Results:** exact baseline versus mitigation comparisons, with the gain calculated as mitigation percent minus baseline percent. 167 rows
- **Performance Linkage Audit:** every mitigation result, including 336 rows with no exact baseline. 503 rows
- **Evidence Quality:** risk-of-bias and credibility judgments for each study. 154 rows
- **Sources:** source and justification for each study. 154 rows

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
- 154 studies, one row each in Study Master and Evidence Quality
- 167 exact performance comparisons
- 336 mitigation results left in the audit
