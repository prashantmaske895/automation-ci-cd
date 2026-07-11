# -*- coding: utf-8 -*-
"""
utils/data_reader.py

Reads data-driven test data from CSV or Excel files and returns a list of
dicts / tuples that pytest.mark.parametrize can consume directly.

Usage:
    from utils.data_reader import read_csv_data, read_excel_data

    data = read_csv_data("data/login_data.csv")
    # -> [{"username": "standard_user", "password": "secret_sauce", ...}, ...]
"""
import os
import csv
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve(path: str) -> str:
    return path if os.path.isabs(path) else os.path.join(PROJECT_ROOT, path)


def read_csv_data(relative_path: str) -> list:
    """Reads a CSV file and returns a list of dicts (one dict per row)."""
    full_path = _resolve(relative_path)
    with open(full_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def read_excel_data(relative_path: str, sheet_name=0) -> list:
    """Reads an Excel file and returns a list of dicts (one dict per row)."""
    full_path = _resolve(relative_path)
    df = pd.read_excel(full_path, sheet_name=sheet_name)
    records = df.to_dict(orient="records")
    # Normalize empty/NaN cells to None explicitly (pandas can leave these
    # as float('nan'), which is truthy in Python and easy to mishandle).
    for row in records:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None
    return records


def as_parametrize_tuples(rows: list, keys: list) -> list:
    """
    Converts a list of dicts into a list of tuples in a fixed key order,
    ready to feed directly into @pytest.mark.parametrize.

    Example:
        rows = read_csv_data("data/login_data.csv")
        cases = as_parametrize_tuples(rows, ["username", "password", "expected_result"])
    """
    def clean(value):
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ""
        return value

    return [tuple(clean(row.get(k)) for k in keys) for row in rows]


if __name__ == "__main__":
    # Quick manual check: python utils/data_reader.py
    print("CSV data:")
    for row in read_csv_data("data/login_data.csv"):
        print(" ", row)

    print("\nExcel data:")
    for row in read_excel_data("data/login_data.xlsx"):
        print(" ", row)
