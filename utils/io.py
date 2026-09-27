from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.constants import ANALYSIS_READY_FILES, RAW_SHEETS
from common.Messages import (
    cannot_serialize,
    configuration_not_found,
    loading_workbook,
    more_columns,
    sheet_size,
    sheets_missing,
    sheets_read,
    tables_missing,
    workbook_loaded,
    workbook_not_found,
)
from common.paths import ANALYSIS_READY_CSV_DIR, DATA_FILE


def read_raw_ard(path: Path = DATA_FILE) -> dict[str, pd.DataFrame]:
    if not path.exists():
        raise FileNotFoundError(workbook_not_found(path))
    workbook = pd.ExcelFile(path, engine="openpyxl")
    missing = [sheet for sheet, _ in RAW_SHEETS.values() if sheet not in workbook.sheet_names]
    if missing:
        raise ValueError(sheets_missing(missing))
    frames = {}
    for key, (sheet, header) in RAW_SHEETS.items():
        frame = pd.read_excel(path, sheet_name=sheet, header=header, engine="openpyxl")
        frames[key] = frame.dropna(axis=0, how="all").dropna(axis=1, how="all")
    return frames


def sample_report(path: Path = DATA_FILE, rows: int = 3, columns: int = 4) -> str:
    frames = read_raw_ard(path)
    lines = [
        loading_workbook(path.name),
        workbook_loaded(path.name),
        sheets_read(len(frames)),
    ]
    for key, frame in frames.items():
        sheet, _ = RAW_SHEETS[key]
        shown = frame.iloc[:, :columns]
        hidden = len(frame.columns) - len(shown.columns)
        lines.append("")
        lines.append(sheet)
        lines.append(sheet_size(len(frame), len(frame.columns)))
        lines.append(shown.head(rows).to_string(index=False))
        if hidden:
            lines.append(more_columns(hidden))
    return "\n".join(lines)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(configuration_not_found(path))
    with path.open("r", encoding="utf-8-sig") as handle:
        return yaml.safe_load(handle)


def ensure_directories(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def save_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=_json_default), encoding="utf-8")


def _json_default(value):
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(cannot_serialize(type(value)))


def load_analysis_ready(directory: Path = ANALYSIS_READY_CSV_DIR) -> dict[str, pd.DataFrame]:
    frames = {}
    missing = []
    for key, filename in ANALYSIS_READY_FILES.items():
        path = directory / filename
        if not path.exists():
            missing.append(filename)
        else:
            frames[key] = pd.read_csv(path)
    if missing:
        raise FileNotFoundError(tables_missing(", ".join(missing)))
    return frames


if __name__ == "__main__":
    sys.stdout.write(sample_report() + "\n")
