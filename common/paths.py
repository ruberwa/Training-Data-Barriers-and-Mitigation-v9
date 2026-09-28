from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "Ready Analysis dataset.xlsx"
CONFIG_DIR = BASE_DIR / "config"
ANALYSIS_CONFIG = CONFIG_DIR / "analysis-config.yaml"
RESULTS_DIR = BASE_DIR / "results"
ANALYSIS_READY_DIR = RESULTS_DIR / "analysis_ready_tables"
ANALYSIS_READY_CSV_DIR = ANALYSIS_READY_DIR / "csv"
VALIDATION_DIR = RESULTS_DIR / "validation"
LOGS_DIR = RESULTS_DIR / "logs"
