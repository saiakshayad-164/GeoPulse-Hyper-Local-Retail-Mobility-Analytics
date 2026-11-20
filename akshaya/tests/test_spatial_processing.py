"""Unit tests for GeoPulse GPS and store input validation."""
import unittest

import pandas as pd

from akshaya.src.spatial_processing import validate_gps_pings, validate_stores


class TestGPSValidation(unittest.TestCase):
    def test_valid_gps_record(self):
        data = pd.DataFrame([{
            "DeviceID": "device-001",
            "Latitude": 17.3850,
            "Longitude": 78.4867,
            "Timestamp": "2026-11-20T10:30:00Z",
        }])
        report = validate_gps_pings(data)
        self.assertTrue(report.loc[0, "is_valid"])
        self.assertEqual(report.loc[0, "issues"], [])

    def test_invalid_gps_values_are_reported(self):
        data = pd.DataFrame([{
            "DeviceID": "",
            "Latitude": 95,
            "Longitude": "not-a-number",
            "Timestamp": "not-a-date",
        }])
        report = validate_gps_pings(data)
        self.assertFalse(report.loc[0, "is_valid"])
        self.assertEqual(
            set(report.loc[0, "issues"]),
            {"missing_DeviceID", "out_of_range_Latitude",
             "invalid_Longitude", "invalid_Timestamp"},
        )

    def test_missing_gps_column_raises_error(self):
        with self.assertRaisesRegex(ValueError, "GPS input missing"):
            validate_gps_pings(pd.DataFrame({"DeviceID": ["d1"]}))


class TestStoreValidation(unittest.TestCase):
    def test_valid_store_record(self):
        data = pd.DataFrame([{
            "Store_ID": "S001",
            "Store_Name": "Central Store",
            "Latitude": 17.3850,
            "Longitude": 78.4867,
        }])
        report = validate_stores(data)
        self.assertTrue(report.loc[0, "is_valid"])
        self.assertEqual(report.loc[0, "issues"], [])

    def test_invalid_store_values_are_reported(self):
        data = pd.DataFrame([{
            "Store_ID": None,
            "Store_Name": " ",
            "Latitude": "north",
            "Longitude": -181,
        }])
        report = validate_stores(data)
        self.assertFalse(report.loc[0, "is_valid"])
        self.assertEqual(
            set(report.loc[0, "issues"]),
            {"missing_Store_ID", "missing_Store_Name",
             "invalid_Latitude", "out_of_range_Longitude"},
        )

    def test_missing_store_column_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Store input missing"):
            validate_stores(pd.DataFrame({"Store_ID": ["S001"]}))


if __name__ == "__main__":
    unittest.main()
