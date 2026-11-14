# GeoPulse – Geospatial Processing

## Member
Akshaya – Member 2: Geospatial Engineering

## Project Overview
GeoPulse is a hyper-local retail mobility analytics project that uses geospatial processing to study movement patterns around retail stores.

## My Responsibilities
- Set up PySpark and Apache Sedona.
- Create 500-meter catchment areas around retail stores.
- Perform spatial joins between GPS location points and store catchment areas.
- Generate structured spatial-join output for the next project stage.
- Test processing performance and document input/output counts and execution time.

## Expected Input Data

### GPS Pings
- DeviceID
- Latitude
- Longitude
- Timestamp

### Store Master
- Store_ID
- Store_Name
- Latitude
- Longitude

## Expected Output
- DeviceID
- Store_ID
- Timestamp
- Inside_Catchment
- Distance_Meters (optional)

## Project Structure
- data/input – Input datasets
- data/output – Generated processing results
- src – Spatial processing source code
- tests – Test cases
- notebooks – Experimentation and analysis

## Current Progress
- Created the Member 2 project folder structure.
- Created initial source, test, and configuration files.
- Created a Python virtual environment.
- PySpark and Apache Sedona setup and compatibility checks are pending.

## Important Note
Processing results and performance metrics will be documented only after actual execution and testing.
