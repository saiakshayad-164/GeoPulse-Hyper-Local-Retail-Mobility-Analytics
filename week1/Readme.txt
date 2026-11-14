GEOPULSE – WEEK 1 README
Member 1: GPS Data Generation & Snowflake Setup

==================================================

1. PROJECT INFORMATION

Project Name: GeoPulse – Hyper-Local Retail Mobility Analytics

Domain: Retail Strategy & Geospatial Analytics

Location: Agra, Uttar Pradesh, India

Week: Week 1

Role: Member 1 – GPS Data Generation & Snowflake Setup

==================================================

2. WEEK 1 OBJECTIVE

The objective of Week 1 was to generate synthetic GPS mobility data, prepare retail store location data, and configure Snowflake for storing geographical information.

==================================================

3. DATASET INFORMATION

A. GPS PINGS DATASET

File Name: agra_gps_pings_100k.csv

Total Records: 100,000

Unique Simulated Devices: Approximately 11,996

Location: Agra, Uttar Pradesh

Columns:
- DeviceID
- Latitude
- Longitude
- Timestamp

B. STORE MASTER DATASET

File Name: agra_store_master.csv

Total Stores: 5

Columns:
- Store_ID
- Store_Name
- Latitude
- Longitude
- Area
- Store_Type

==================================================

4. SNOWFLAKE DATABASE SETUP

Database Name: GEOPULSE_DB

Schema Name: RAW

The following tables were created:

1. GPS_PINGS_STG
2. STORE_MASTER_STG
3. GPS_PINGS
4. STORE_MASTER

The staging tables store the uploaded CSV data.

The final tables contain geographical information using Snowflake GEOGRAPHY data type.

==================================================

5. GEOGRAPHICAL DATA CONVERSION

The GPS coordinates and store coordinates were converted into geographical points using:

ST_MAKEPOINT(LONGITUDE, LATITUDE)

Longitude is passed first, followed by latitude.

The final tables contain a LOCATION column with GEOGRAPHY values.

==================================================

6. WEEK 1 COMPLETED TASKS

[Completed] Generated 100,000 synthetic GPS records.

[Completed] Prepared 5 demo retail store locations.

[Completed] Created Snowflake database GEOPULSE_DB.

[Completed] Created RAW schema.

[Completed] Created GPS staging table.

[Completed] Created Store Master staging table.

[Completed] Created final GPS geographical table.

[Completed] Created final Store Master geographical table.

[Completed] Converted coordinates into GEOGRAPHY points.

==================================================

7. FILE STRUCTURE

Week_1/
|
|-- Data/
|   |-- agra_gps_pings_100k.csv
|   |-- agra_store_master.csv
|
|-- SQL/
|   |-- geopulse_snowflake_setup.sql
|
|-- README.txt

==================================================

8. IMPORTANT NOTES

- All GPS records are synthetic.
- Device IDs are simulated identifiers, not actual personal identifiers.
- Store locations are fictional demo locations.
- The dataset is intended only for academic and project analysis.
- No real individual movement data has been collected.

==================================================

9. WEEK 1 STATUS

STATUS: COMPLETED

Week 1 deliverables cover synthetic GPS data generation, store master preparation, Snowflake database configuration, staging tables, final geographical tables and coordinate conversion.

==================================================

GeoPulse – Hyper-Local Retail Mobility Analytics
Member 1 – Week 1 Deliverables
