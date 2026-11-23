# Week 2 Day 5 - Kepler.gl Footfall Visualization & Review Notes

## 1. Dataset & Configuration
- **Source Model:** `GEOPULSE_DB.PUBLIC.FCT_STORE_FOOTFALL` (803 exported rows)
- **Heatmap Layer:** Plotted using `store_lat` and `store_lon`, weighted by `unique_visitors` within the 500m catchment radius.
- **Time-Based View:** Configured temporal filter on `hour` to observe visitor shifts across Morning, Afternoon, Evening, and Night windows.

## 2. Key Observations
- **Peak Footfall Windows:** Afternoon (12:00-17:00) and Evening (18:00-22:00) show higher `unique_visitors` and `total_pings` compared to early morning and night hours.
- **Store Catchment Distribution:** Existing stores in dense commercial areas show sustained footfall, while proposed locations capture distinct regional traffic.
- **Data Quality Validation:** All 15 dbt schema and data quality tests passed (`PASS=15, WARN=0, ERROR=0`) prior to export.

## 3. Artifacts Included
- `viz/fct_store_footfall.csv`
- `viz/kepler_footfall_heatmap.png`
- `viz/kepler_time_view.png`
- `viz/kepler_footfall_config.json`