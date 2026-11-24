"""Small synthetic benchmark harness for baseline spatial join.

Run from repository root: python -m akshaya.src.benchmark_spatial_join
The results are measurements from this local baseline, not Spark benchmarks.
"""
import time
import pandas as pd
from akshaya.src.spatial_join import spatial_join_gps_to_stores


def make_inputs(ping_count, store_count=20):
    stores = pd.DataFrame([
        {"Store_ID": f"S{i:04}", "Store_Name": f"Store {i}",
         "Latitude": 17.30 + (i * 0.002), "Longitude": 78.40 + (i * 0.002)}
        for i in range(store_count)
    ])
    gps = pd.DataFrame([
        {"DeviceID": f"D{i:07}", "Latitude": 17.30 + ((i % 1000) * 0.0001),
         "Longitude": 78.40 + ((i % 1000) * 0.0001),
         "Timestamp": "2026-11-24T10:00:00Z"}
        for i in range(ping_count)
    ])
    return gps, stores


def run_benchmarks(sizes=(100, 500, 1000), store_count=20):
    rows = []
    for size in sizes:
        gps, stores = make_inputs(size, store_count)
        start = time.perf_counter()
        output = spatial_join_gps_to_stores(gps, stores)
        elapsed = time.perf_counter() - start
        rows.append({"gps_rows": size, "store_rows": store_count,
                     "output_rows": len(output), "elapsed_seconds": round(elapsed, 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(run_benchmarks().to_string(index=False))
