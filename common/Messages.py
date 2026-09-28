def loading_workbook(name):
    return f"Loading analysis-ready dataset: {name}"


def workbook_not_found(path):
    return f"Input workbook not found: {path}"


def sheets_missing(missing):
    return f"Analysis-ready dataset is missing required sheets: {missing}"


def workbook_loaded(name):
    return f"Workbook: {name}"


def sheets_read(count):
    return f"Sheets read: {count}"


def sheet_size(rows, columns):
    return f"Rows: {rows}  Columns: {columns}"


def more_columns(count):
    return f"... {count} more columns"


def phase1_description():
    return "Create analysis-ready tables from the analysis-ready dataset"


def data_argument_help():
    return "Path to the analysis-ready dataset workbook"


def loading_configuration(path):
    return f"Loading analysis configuration: {path}"


def configuration_not_found(path):
    return f"Analysis configuration not found: {path}"


def sheets_loaded(count):
    return f"Loaded {count} source sheets"


def building_tables():
    return "Building analysis-ready tables"


def tables_built(count):
    return f"Built {count} analysis-ready tables"


def writing_table(index, total, name, rows):
    return f"[{index}/{total}] Writing {name} ({rows} rows)"


def writing_workbook(path):
    return f"Writing combined workbook: {path}"


def running_validation():
    return "Running validation"


def phase_complete():
    return "Analysis-ready tables complete"


def source_studies(count):
    return f"Source studies: {count}"


def barrier_mitigation_rows(count):
    return f"Barrier-mitigation rows: {count}"


def exact_linked_rows(count):
    return f"Linked performance rows: {count}"


def validation_status(status):
    return f"Validation status: {status}"


def output_workbook(path):
    return f"Output workbook: {path}"


def csv_directory(path):
    return f"CSV directory: {path}"


def validation_failed(path):
    return f"Validation failed. Inspect {path}"


def phase_started(name):
    return f"{name} started"


def progress_log(path):
    return f"Progress log: {path}"


def study_master_row_mismatch():
    return "Study master does not preserve one row per identification record"


def study_master_duplicate():
    return "Study master contains duplicate Study IDs"


def quality_duplicate():
    return "Evidence quality contains duplicate Study IDs"


def no_exact_comparisons():
    return "No exact baseline-mitigation performance comparisons were created"


def cannot_serialize(kind):
    return f"Cannot serialize {kind}"


def tables_missing(names):
    return (
        f"Analysis-ready tables are missing: {names}. "
        "Run src/01_create_analysis_ready_tables.py first."
    )
