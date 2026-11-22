"""Tests for baseline GPS/store spatial matching."""
import unittest
import pandas as pd
from akshaya.src.spatial_join import spatial_join_gps_to_stores, OUTPUT_COLUMNS


class TestSpatialJoin(unittest.TestCase):
    def setUp(self):
        self.stores = pd.DataFrame([
            {"Store_ID":"S1", "Store_Name":"Near", "Latitude":17.385, "Longitude":78.4867},
            {"Store_ID":"S2", "Store_Name":"Far", "Latitude":17.40, "Longitude":78.50},
        ])

    def test_ping_inside_near_store(self):
        gps = pd.DataFrame([{"DeviceID":"D1","Latitude":17.3851,"Longitude":78.4867,"Timestamp":"2026-11-22T10:00:00Z"}])
        result = spatial_join_gps_to_stores(gps, self.stores)
        self.assertEqual(list(result.columns), OUTPUT_COLUMNS)
        self.assertTrue(result.loc[0, "Inside_Catchment"])
        self.assertEqual(result.loc[0, "Store_ID"], "S1")

    def test_outside_ping_is_retained_as_nearest(self):
        gps = pd.DataFrame([{"DeviceID":"D2","Latitude":17.8,"Longitude":78.9,"Timestamp":"2026-11-22T10:00:00Z"}])
        result = spatial_join_gps_to_stores(gps, self.stores)
        self.assertEqual(len(result), 1)
        self.assertFalse(result.loc[0, "Inside_Catchment"])
        self.assertGreater(result.loc[0, "Distance_Meters"], 500)

    def test_ping_matching_multiple_catchments_returns_multiple_rows(self):
        stores = pd.DataFrame([
            {"Store_ID":"S1","Store_Name":"A","Latitude":17.385,"Longitude":78.4867},
            {"Store_ID":"S2","Store_Name":"B","Latitude":17.3851,"Longitude":78.4867},
        ])
        gps = pd.DataFrame([{"DeviceID":"D3","Latitude":17.385,"Longitude":78.4867,"Timestamp":"now"}])
        result = spatial_join_gps_to_stores(gps, stores)
        self.assertEqual(len(result), 2)
        self.assertTrue(result["Inside_Catchment"].all())

    def test_empty_store_input_fails(self):
        with self.assertRaisesRegex(ValueError, "at least one store"):
            spatial_join_gps_to_stores(pd.DataFrame(columns=["DeviceID","Latitude","Longitude","Timestamp"]), self.stores.iloc[0:0])

    def test_invalid_radius_fails(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            spatial_join_gps_to_stores(pd.DataFrame(columns=["DeviceID","Latitude","Longitude","Timestamp"]), self.stores, 0)


if __name__ == "__main__":
    unittest.main()
