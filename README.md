# GeoPulse: Hyper-Local Retail Mobility Analytics

**Project Domain:** Retail Strategy & Geospatial Analytics

## Project Overview

GeoPulse is a geospatial analytics project designed to analyze synthetic, anonymized GPS mobility data and understand hyper-local retail movement patterns.

The project focuses on analyzing location-based footfall around existing and proposed retail stores, identifying potential traffic overlap, and supporting data-driven retail location decisions.

## Project Objectives

- Generate and analyze synthetic GPS location data.
- Prepare retail store location information.
- Store and manage geographical data.
- Analyze GPS points in relation to store catchment areas.
- Calculate hourly footfall patterns.
- Identify potential traffic overlap between retail locations.
- Support retail expansion and location planning decisions.

## Project Technology Stack

| Technology | Purpose |
|---|---|
| Snowflake | Cloud data warehouse and geographical data storage |
| SQL | Data preparation, transformation and validation |
| Python | Synthetic GPS data generation |
| PySpark | Large-scale data processing |
| Apache Sedona | Geospatial processing |
| dbt | Data transformation and modelling |
| Kepler.gl | Geospatial data visualization |

## Project Dataset

The project uses synthetic GPS mobility data generated for Agra, Uttar Pradesh.

### GPS Dataset

- Total GPS records: 100,000
- Unique simulated devices: Approximately 11,996
- Location: Agra, Uttar Pradesh
- Data fields:
  - DeviceID
  - Latitude
  - Longitude
  - Timestamp

### Store Master Dataset

The store master dataset contains 5 fictional demo retail locations across selected areas of Agra.

Data fields:
- Store_ID
- Store_Name
- Latitude
- Longitude
- Area
- Store_Type

**Note:** All GPS records and demo store locations are synthetic and created for academic project purposes. They do not represent actual individual movements or verified retail businesses.

## Team Responsibilities

The project is divided among three team members:

| Member | Responsibilities |
|---|---|
| Member 1 | GPS Data Generation and Snowflake Setup |
| Member 2 | PySpark and Apache Sedona Geospatial Processing |
| Member 3 | dbt Transformation and Kepler.gl Visualization |

## Repository Structure

```text
GeoPulse/
│
├── README.md
│
└── Week_1/
    ├── Data/
    │   ├── agra_gps_pings_100k.csv
    │   └── agra_store_master.csv
    │
    ├── SQL/
    │   └── geopulse_snowflake_setup.sql
    │
    └── README.txt
```

## Member 1: Week 1 Progress

The following tasks have been completed:

- Generated 100,000 synthetic GPS records for Agra.
- Prepared a store master dataset containing 5 demo stores.
- Created the Snowflake database and RAW schema.
- Created GPS and Store Master staging tables.
- Created final GPS and Store Master tables.
- Converted latitude and longitude coordinates into Snowflake GEOGRAPHY points using `ST_MAKEPOINT()`.

### Snowflake Database Structure

```text
GEOPULSE_DB
│
└── RAW
    ├── GPS_PINGS_STG
    ├── STORE_MASTER_STG
    ├── GPS_PINGS
    └── STORE_MASTER
```

## Expected Project Outcome

GeoPulse aims to provide insights into:

- Hourly retail footfall patterns.
- Geographical movement around retail stores.
- Store catchment area analysis.
- Potential traffic overlap between existing and proposed stores.
- Data-supported retail location decisions.

**Important:** Geographical traffic overlap indicates potential customer movement overlap. It does not independently prove sales cannibalization without supporting sales data.

## Project Status

**Week 1 – GPS Data Generation and Snowflake Setup: Completed**

Further data validation, geospatial processing, transformation and visualization activities will be carried out in subsequent project phases.

---

**Academic Project:** GeoPulse – Hyper-Local Retail Mobility Analytics

**Location:** Agra, Uttar Pradesh, India
