"""Utilities for validating GeoPulse inputs and reporting validation summaries."""
import pandas as pd

GPS_REQUIRED = ["DeviceID", "Latitude", "Longitude", "Timestamp"]
STORE_REQUIRED = ["Store_ID", "Store_Name", "Latitude", "Longitude"]


def _check_columns(df, required, kind):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{kind} input missing required columns: {missing}")


def _validate_coordinates(row, problems):
    for col, lo, hi in (("Latitude", -90, 90), ("Longitude", -180, 180)):
        value = pd.to_numeric(row[col], errors="coerce")
        if pd.isna(value):
            problems.append(f"invalid_{col}")
        elif not lo <= value <= hi:
            problems.append(f"out_of_range_{col}")


def validate_gps_pings(df):
    """Produce row-level validity and issue details without changing input."""
    _check_columns(df, GPS_REQUIRED, "GPS")
    reports = []
    for idx, row in df.iterrows():
        problems = []
        if pd.isna(row["DeviceID"]) or not str(row["DeviceID"]).strip():
            problems.append("missing_DeviceID")
        _validate_coordinates(row, problems)
        if pd.isna(pd.to_datetime(row["Timestamp"], errors="coerce", utc=True)):
            problems.append("invalid_Timestamp")
        reports.append({"row_index": idx, "is_valid": not problems, "issues": problems})
    return pd.DataFrame(reports, columns=["row_index", "is_valid", "issues"])


def validate_stores(df):
    """Produce row-level validity and issue details for store master records."""
    _check_columns(df, STORE_REQUIRED, "Store")
    reports = []
    for idx, row in df.iterrows():
        problems = []
        for col in ("Store_ID", "Store_Name"):
            if pd.isna(row[col]) or not str(row[col]).strip():
                problems.append(f"missing_{col}")
        _validate_coordinates(row, problems)
        reports.append({"row_index": idx, "is_valid": not problems, "issues": problems})
    return pd.DataFrame(reports, columns=["row_index", "is_valid", "issues"])


def validation_summary(report):
    """Summarize row validation results and count each issue type."""
    if not {"is_valid", "issues"}.issubset(report.columns):
        raise ValueError("Validation report must contain is_valid and issues columns")
    total = len(report)
    valid = int(report["is_valid"].fillna(False).sum())
    issue_counts = {}
    for issues in report["issues"]:
        if isinstance(issues, (list, tuple)):
            for issue in issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
    return {
        "total_rows": total,
        "valid_rows": valid,
        "invalid_rows": total - valid,
        "issue_counts": issue_counts,
    }
