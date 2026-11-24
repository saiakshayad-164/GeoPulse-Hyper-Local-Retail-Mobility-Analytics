"""Tests for validation summary and output export utilities."""
import tempfile
import unittest
from pathlib import Path
import pandas as pd

from akshaya.src.spatial_processing import validation_summary
from akshaya.src.spatial_join import write_spatial_join_csv, OUTPUT_COLUMNS


class TestValidationSummary(unittest.TestCase):
    def test_summary_counts_rows_and_issues(self):
        report = pd.DataFrame([
            {"is_valid": True, "issues": []},
            {"is_valid": False, "issues": ["invalid_Latitude", "invalid_Timestamp"]},
            {"is_valid": False, "issues": ["invalid_Latitude"]},
        ])
        summary = validation_summary(report)
        self.assertEqual(summary["total_rows"], 3)
        self.assertEqual(summary["valid_rows"], 1)
        self.assertEqual(summary["invalid_rows"], 2)
        self.assertEqual(summary["issue_counts"]["invalid_Latitude"], 2)


class TestCSVExport(unittest.TestCase):
    def test_export_schema_and_boolean_values(self):
        frame = pd.DataFrame([
            {"DeviceID":"D1","Store_ID":"S1","Timestamp":"2026-11-24T09:00:00Z",
             "Inside_Catchment":True,"Distance_Meters":12.5}
        ])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.csv"
            write_spatial_join_csv(frame, path)
            loaded = pd.read_csv(path)
        self.assertEqual(list(loaded.columns), OUTPUT_COLUMNS)
        self.assertTrue(bool(loaded.loc[0, "Inside_Catchment"]))
        self.assertAlmostEqual(loaded.loc[0, "Distance_Meters"], 12.5)


if __name__ == "__main__":
    unittest.main()
