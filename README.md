# GeoPulse: Hyper-Local Retail Mobility Analytics

## Role: Geospatial BI & Analytics (Member 3)
- **Data Warehouse:** Snowflake
- **Data Modeling:** dbt
- **Geospatial Visualization:** Kepler.gl

### Week 1 Progress
- [x] Day 1: Set up `geopulse_dbt` project structure and configuration.
- [x] Day 2: Configure Snowflake source definitions (`sources.yml`).
- [x] Day 3: Build staging SQL models (`stg_gps_pings.sql` & `stg_stores.sql`) with geospatial point conversion.
- [x] Day 4: Build core geospatial mart models (`fct_store_footfall.sql` & `fct_cannibalization_metrics.sql`).
- [x] Day 5: Add dbt schema documentation and automated data quality tests (`stg_schema.yml` & `marts_schema.yml`).

### Week 2 Progress
- [x] Day 1: Refine staging models (`stg_gps_pings` & `stg_stores`) and validate coordinate/timestamp standardization.
- [x] Day 2: Implement 500m Haversine spatial join and hourly footfall aggregations in `fct_store_footfall.sql`.
- [x] Day 3: Add time-of-day segmentation (`Morning`, `Afternoon`, `Evening`, `Night`) and store traffic metrics (`unique_visitors`, `total_pings`, `avg_distance_meters`).
- [x] Day 4: Execute `dbt build` and verify all 15 schema and data quality tests (`PASS=15, WARN=0, ERROR=0`).
- [x] Day 5: Export footfall mart (`viz/fct_store_footfall.csv` — 803 rows), generate Kepler.gl heatmap & temporal views (`viz/kepler_footfall_heatmap.png`, `viz/kepler_time_view.png`, `viz/kepler_footfall_config.json`), and document insights (`viz/review_notes.md`).