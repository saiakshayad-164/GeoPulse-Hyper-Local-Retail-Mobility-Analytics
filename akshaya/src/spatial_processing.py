"""Validation utilities for GeoPulse GPS and store inputs."""
import pandas as pd

GPS_REQUIRED = ["DeviceID", "Latitude", "Longitude", "Timestamp"]
STORE_REQUIRED = ["Store_ID", "Store_Name", "Latitude", "Longitude"]


def _check_columns(df, required, kind):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{kind} input missing required columns: {missing}")


def validate_gps_pings(df):
    """Produce row-level validity and issue details without changing input."""
    _check_columns(df, GPS_REQUIRED, "GPS")
    reports = []
    for idx, row in df.iterrows():
        problems = []
        if pd.isna(row["DeviceID"]) or not str(row["DeviceID"]).strip():
            problems.append("missing_DeviceID")
        for col, lo, hi in (("Latitude", -90, 90), ("Longitude", -180, 180)):
            value = pd.to_numeric(row[col], errors="coerce")
            if pd.isna(value):
                problems.append(f"invalid_{col}")
            elif not lo <= value <= hi:
                problems.append(f"out_of_range_{col}")
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
        for col, lo, hi in (("Latitude", -90, 90), ("Longitude", -180, 180)):
            value = pd.to_numeric(row[col], errors="coerce")
            if pd.isna(value):
                problems.append(f"invalid_{col}")
            elif not lo <= value <= hi:
                problems.append(f"out_of_range_{col}")
        reports.append({"row_index": idx, "is_valid": not problems, "issues": problems})
    return pd.DataFrame(reports, columns=["row_index", "is_valid", "issues"])
