# Baseline spatial join benchmark procedure

Run the synthetic harness from the repository root:

```powershell
python -m akshaya.src.benchmark_spatial_join
```

It runs the baseline join for 100, 500 and 1,000 GPS pings against 20 synthetic stores and reports input size, output row count and elapsed seconds. These figures are measurements only when the script is actually run; no results are recorded here.

The baseline implementation is Python/Pandas with geodesic distance calculations and is intended for functional checks and small-scale measurements. It is not a substitute for Spark/Sedona scale testing.
