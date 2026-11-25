"""Tests for chunked vectorized spatial matching."""
import unittest
import pandas as pd
from akshaya.src.spatial_join import spatial_join_gps_to_stores, spatial_join_chunks, OUTPUT_COLUMNS


class TestChunkedSpatialJoin(unittest.TestCase):
    def setUp(self):
        self.stores = pd.DataFrame([
            {"Store_ID":"S1", "Store_Name":"Near", "Latitude":17.385, "Longitude":78.4867},
            {"Store_ID":"S2", "Store_Name":"Far", "Latitude":17.40, "Longitude":78.50},
        ])
        self.gps = pd.DataFrame([
            {"DeviceID":"D1","Latitude":17.3851,"Longitude":78.4867,"Timestamp":"t1"},
            {"DeviceID":"D2","Latitude":17.8,"Longitude":78.9,"Timestamp":"t2"},
            {"DeviceID":"D3","Latitude":17.385,"Longitude":78.4867,"Timestamp":"t3"},
        ])

    def test_chunked_results_equal_full_join(self):
        full = spatial_join_gps_to_stores(self.gps, self.stores)
        chunks = pd.concat(list(spatial_join_chunks(self.gps, self.stores, chunk_size=1)), ignore_index=True)
        pd.testing.assert_frame_equal(full.reset_index(drop=True), chunks.reset_index(drop=True))

    def test_chunk_sizes_preserve_all_pings(self):
        chunks = list(spatial_join_chunks(self.gps, self.stores, chunk_size=2))
        self.assertEqual(len(chunks), 2)
        self.assertEqual(sum(len(x) for x in chunks), len(spatial_join_gps_to_stores(self.gps, self.stores)))

    def test_invalid_chunk_size(self):
        with self.assertRaisesRegex(ValueError, "at least 1"):
            list(spatial_join_chunks(self.gps, self.stores, chunk_size=0))

    def test_output_columns(self):
        result = spatial_join_gps_to_stores(self.gps, self.stores)
        self.assertEqual(list(result.columns), OUTPUT_COLUMNS)


if __name__ == "__main__":
    unittest.main()
