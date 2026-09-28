**Title:** Set up the analysis of training-data barriers and mitigation strategies

## Project status
- Studies training-data barriers and mitigation strategies in weed detection, segmentation, and classification
- Source dataset and country map are in place
- Analysis-ready tables are built from the source workbook

## Folders
- 9 folders

- `Docs`: project documents, including setup and installation
  - `01_Project-Setup.md`: what this project is and what is in the repository now
  - `02_Installation.md`: how to install Python and the project packages
  - `03_Analysis-Ready-Tables.md`: how the source workbook becomes the analysis-ready tables
- `common`: shared paths and names used by every phase
  - `__init__.py`: marks this folder as a Python package
  - `constants.py`: sheet names, analysis-ready filenames, and the Synthetic Image Methods set
  - `paths.py`: locations of the workbook, settings, map, and output folders
- `config`: settings for the analysis, figures, and research questions
  - `analysis-config.yaml`: task order, primary metrics, random seed, repetitions, and sensitivity rules
  - `figures-config.yaml`: figure sizes, colors, filenames, and output formats
  - `research-question-map.yaml`: which tables and figures answer each research question
- `data`: the analysis-ready dataset
  - `Ready Analysis dataset.xlsx`: source record of the included studies
- `data/maps`: country boundaries for the geographic view
  - `naturalearth_lowres.shp`: country shapes
  - `naturalearth_lowres.shx`: shape index
  - `naturalearth_lowres.dbf`: country attributes
  - `naturalearth_lowres.prj`: map projection
  - `naturalearth_lowres.cpg`: text encoding for the country names
- `utils`: reading, writing, statistics, plotting, logging, and validation
  - `__init__.py`: marks this folder as a Python package
  - `io.py`: reads the workbook and settings, and writes CSV and JSON
  - `statistics.py`: bootstrap intervals, permutation tests, and study-level gains
  - `plotting.py`: figure style and saving PNG, PDF, and TIFF
  - `progress.py`: timestamped progress logs for each phase
  - `validation.py`: checks the register, eligible gains, and one row per study
- `results`: outputs written when the analysis runs
  - `analysis_ready_tables/analysis_ready_tables.xlsx`: the analysis-ready tables in one workbook
  - `analysis_ready_tables/csv/study_master.csv`: one row per study
  - `analysis_ready_tables/csv/barrier_profile.csv`: each coded barrier, with the study task
  - `analysis_ready_tables/csv/mitigation_profile.csv`: each coded mitigation, with the study task
  - `analysis_ready_tables/csv/barrier_mitigation_cooccurrence.csv`: same-instance co-occurrence within a paper
  - `analysis_ready_tables/csv/comparison_register.csv`: one row per baseline context, with its selection status
  - `analysis_ready_tables/csv/performance_results.csv`: eligible comparisons, with the signed gain
  - `analysis_ready_tables/csv/performance_linkage_audit.csv`: every tab 8 row, including rows that were not selected
  - `analysis_ready_tables/csv/evidence_quality.csv`: risk-of-bias and credibility judgments
  - `logs/analysis_ready_tables.log`: progress record for the analysis-ready tables
  - `validation/analysis_ready_tables.json`: pass or fail record for the analysis-ready tables
- `src`: the three phase scripts
  - `__init__.py`: marks this folder as a Python package
  - `01_create_analysis_ready_tables.py`: builds the analysis-ready tables from the workbook
  - `02_create_statistical_results.py`: computes the research-question statistics from those tables
  - `03_create_figures.py`: draws the figures from the saved statistics
- `src/analysis`: table building, statistical results, and figures
  - `__init__.py`: marks this folder as a Python package
  - `prepare_tables.py`: builds the study, coding, and comparison tables from the workbook
  - `statistical_pipeline.py`: builds the descriptive and research-question tables
  - `figures.py`: draws each publication figure

## Root files
- 3 files
- `.gitignore`: keeps `PR-Description.md` out of Git
- `README.md`: project title
- `requirements.txt`: Python packages the analysis needs

## What is included
- Analysis-ready dataset, the source record of the included studies
- Country boundaries for the geographic view of those studies

## Test plan
- [ ] Source workbook and country map are available
