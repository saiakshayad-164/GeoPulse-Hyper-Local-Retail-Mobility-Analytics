"""Tests for metric store catchment construction."""
import unittest
import pandas as pd
from shapely.geometry import Point
from pyproj import CRS, Transformer
from shapely.ops import transform

from akshaya.src.catchments import build_store_catchments


class TestCatchments(unittest.TestCase):
    def setUp(self):
        self.stores = pd.DataFrame([{
            "Store_ID": "S001", "Store_Name": "Test Store",
            "Latitude": 17.385, "Longitude": 78.4867,
        }])

    def test_returns_wgs84_polygon_and_metadata(self):
        result = build_store_catchments(self.stores)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "Store_ID"], "S001")
        self.assertTrue(result.loc[0, "geometry"].is_valid)
        self.assertEqual(result.loc[0, "geometry"].geom_type, "Polygon")

    def test_buffer_radius_is_approximately_500_metres(self):
        result = build_store_catchments(self.stores)
        polygon = result.loc[0, "geometry"]
        lon, lat = 78.4867, 17.385
        local = CRS.from_proj4(f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs")
        forward = Transformer.from_crs("EPSG:4326", local, always_xy=True).transform
        metric = transform(forward, polygon)
        self.assertAlmostEqual(metric.bounds[2], 500, delta=1)
        self.assertAlmostEqual(metric.bounds[0], -500, delta=1)

    def test_rejects_nonpositive_radius(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            build_store_catchments(self.stores, radius_m=0)

    def test_missing_columns_raise_error(self):
        with self.assertRaisesRegex(ValueError, "missing required"):
            build_store_catchments(pd.DataFrame({"Store_ID": ["S001"]}))


if __name__ == "__main__":
    unittest.main()
