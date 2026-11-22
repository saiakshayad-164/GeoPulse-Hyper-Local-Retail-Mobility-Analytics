# GeoPulse – Geospatial Processing

## Member
Akshaya – Member 2: Geospatial Engineering

## Project Overview
GeoPulse is a hyper-local retail mobility analytics project that uses geospatial processing to study movement patterns around retail stores.

## Responsibilities
- Create 500-meter catchment areas around stores.
- Match GPS pings against store catchments.
- Export the agreed spatial output for downstream analysis.
- Validate input data and report issues.
- Test performance and document measured results.

## Input Data
GPS pings: `DeviceID`, `Latitude`, `Longitude`, `Timestamp`.

Store master: `Store_ID`, `Store_Name`, `Latitude`, `Longitude`.

## Output Schema
- `DeviceID`
- `Store_ID`
- `Timestamp`
- `Inside_Catchment`
- `Distance_Meters`

## Implemented modules
- `src/spatial_processing.py`: GPS/store row validation and validation summary.
- `src/catchments.py`: circular catchment polygon construction with a metric local projection and WGS84 output.
- `src/spatial_join.py`: baseline geodesic distance matching and CSV writer.
- `tests/`: unit test files for validation, catchment construction and spatial matching.

## Spatial join semantics
A ping inside one or more catchments produces one row per matched store. A ping outside all catchments is retained once with its nearest store, `Inside_Catchment=False`, and the distance. This is a baseline functional implementation, not a distributed Spark/Sedona processing pipeline.

## Setup
The dependencies are listed in `requirements.txt`. Use the project virtual environment and run tests from the repository root after installing dependencies.

## Current status
The baseline validation, catchment-generation, spatial-match, CSV-export utilities and test cases have been added. Execution of the test suite, real-data output generation, Spark/Sedona runtime resolution, and performance benchmarking remain to be verified. No measured record counts, runtimes or file sizes are reported until actual runs are completed.

## Project structure
- `data/input`: input datasets
- `data/output`: generated results
- `src`: processing modules
- `tests`: test cases
- `notebooks`: experiments
- `docs`: progress notes
