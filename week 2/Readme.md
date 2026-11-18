# GeoPulse – Week 2
## Member 1: GPS Data Generation & Snowflake

### Objective
The objective of Week 2 was to validate the synthetic GPS dataset, verify data quality, and confirm successful spatial data storage in Snowflake.

### Data Validation Results

| Validation | Result |
|---|---:|
| Total GPS Records | 100,000 |
| Total Stores | 5 |
| Missing Values | 0 |
| Duplicate GPS Records | 0 |
| Invalid Coordinates | 0 |
| Invalid Timestamps | 0 |

### Snowflake Verification

Database: `GEOPULSE_DB`

Schema containing the tables: `PUBLIC`

Verified tables:
- `GPS_PINGS`
- `STORE_MASTER`
- `GPS_PINGS_STG`
- `STORE_MASTER_STG`

### Spatial Data Verification
- Verified GPS location data using `ST_ASWKT(LOCATION)`.
- Verified store location data using `ST_ASWKT(LOCATION)`.
- Successfully executed sample queries without SQL errors.
- Confirmed that the GEOGRAPHY column contains readable spatial representations.

### Week 2 Deliverables
1. GPS data quality validation.
2. Duplicate and missing-value checks.
3. Coordinate and timestamp validation.
4. Snowflake table verification.
5. GEOGRAPHY column verification.
6. SQL validation documentation.

### Conclusion
Week 2 validation was completed successfully. The dataset contains 100,000 synthetic GPS records and 5 store records. No missing values, duplicate GPS records, invalid coordinates, or invalid timestamps were reported.

The Snowflake tables and spatial location data were successfully verified. The dataset is ready for integration with the spatial processing workflow handled by the other team members.

**Note:** All GPS records are synthetic and anonymized simulation data, not real customer tracking data.
