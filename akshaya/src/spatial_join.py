"""Baseline GPS-to-store catchment matching using geodesic distances."""
import pandas as pd
from pyproj import Geod

GPS_REQUIRED = ["DeviceID", "Latitude", "Longitude", "Timestamp"]
STORE_REQUIRED = ["Store_ID", "Store_Name", "Latitude", "Longitude"]
OUTPUT_COLUMNS = ["DeviceID", "Store_ID", "Timestamp", "Inside_Catchment", "Distance_Meters"]

_GEOD = Geod(ellps="WGS84")


def spatial_join_gps_to_stores(gps, stores, radius_m=500):
    """Match each ping to every store within radius, preserving unmatched pings.

    If a ping is outside every catchment, retain it once with the nearest store,
    Inside_Catchment=False, and its distance, so downstream consumers can audit
    non-matches. Distances use the WGS84 ellipsoid and are in meters.
    """
    for df, required, label in ((gps, GPS_REQUIRED, "GPS"), (stores, STORE_REQUIRED, "Store")):
        missing = sorted(set(required) - set(df.columns))
        if missing:
            raise ValueError(f"{label} input missing required columns: {missing}")
    if radius_m <= 0:
        raise ValueError("radius_m must be positive")
    if stores.empty:
        raise ValueError("Store input must contain at least one store")

    store_records = []
    for _, store in stores.iterrows():
        lat = pd.to_numeric(store["Latitude"], errors="coerce")
        lon = pd.to_numeric(store["Longitude"], errors="coerce")
        if pd.isna(lat) or pd.isna(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise ValueError(f"Invalid coordinates for store {store['Store_ID']}")
        store_records.append((store["Store_ID"], float(lat), float(lon)))

    results = []
    for _, ping in gps.iterrows():
        lat = pd.to_numeric(ping["Latitude"], errors="coerce")
        lon = pd.to_numeric(ping["Longitude"], errors="coerce")
        if pd.isna(lat) or pd.isna(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise ValueError(f"Invalid GPS coordinates at row {ping.name}")
        distances = []
        for store_id, store_lat, store_lon in store_records:
            _, _, distance = _GEOD.inv(float(lon), float(lat), store_lon, store_lat)
            distances.append((store_id, distance))
        matches = [(sid, dist) for sid, dist in distances if dist <= radius_m]
        if matches:
            for sid, dist in matches:
                results.append({
                    "DeviceID": ping["DeviceID"], "Store_ID": sid,
                    "Timestamp": ping["Timestamp"], "Inside_Catchment": True,
                    "Distance_Meters": float(dist),
                })
        else:
            sid, dist = min(distances, key=lambda item: item[1])
            results.append({
                "DeviceID": ping["DeviceID"], "Store_ID": sid,
                "Timestamp": ping["Timestamp"], "Inside_Catchment": False,
                "Distance_Meters": float(dist),
            })
    output = pd.DataFrame(results, columns=OUTPUT_COLUMNS)
    output["Inside_Catchment"] = output["Inside_Catchment"].astype(bool)
    output["Distance_Meters"] = output["Distance_Meters"].astype(float)
    return output


def write_spatial_join_csv(result, output_path):
    """Write the standardized output CSV without the DataFrame index."""
    missing = sorted(set(OUTPUT_COLUMNS) - set(result.columns))
    if missing:
        raise ValueError(f"Spatial join output missing columns: {missing}")
    result.loc[:, OUTPUT_COLUMNS].to_csv(output_path, index=False)
