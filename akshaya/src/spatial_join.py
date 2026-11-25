"""Baseline GPS-to-store matching using chunked vectorized geodesic distances."""
import pandas as pd
from pyproj import Geod

GPS_REQUIRED = ["DeviceID", "Latitude", "Longitude", "Timestamp"]
STORE_REQUIRED = ["Store_ID", "Store_Name", "Latitude", "Longitude"]
OUTPUT_COLUMNS = ["DeviceID", "Store_ID", "Timestamp", "Inside_Catchment", "Distance_Meters"]
_GEOD = Geod(ellps="WGS84")


def _prepare_stores(stores):
    missing = sorted(set(STORE_REQUIRED) - set(stores.columns))
    if missing:
        raise ValueError(f"Store input missing required columns: {missing}")
    if stores.empty:
        raise ValueError("Store input must contain at least one store")
    prepared = []
    for _, store in stores.iterrows():
        lat = pd.to_numeric(store["Latitude"], errors="coerce")
        lon = pd.to_numeric(store["Longitude"], errors="coerce")
        if pd.isna(lat) or pd.isna(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise ValueError(f"Invalid coordinates for store {store['Store_ID']}")
        prepared.append((store["Store_ID"], float(lat), float(lon)))
    return prepared


def spatial_join_chunks(gps, stores, radius_m=500, chunk_size=1000):
    """Yield output DataFrames for GPS chunks, limiting intermediate memory.

    For each ping, vectorized Geod distance calculations compare it with every
    store. Pings inside one or more catchments generate one row per match;
    unmatched pings are retained once with their nearest store and distance.
    """
    missing = sorted(set(GPS_REQUIRED) - set(gps.columns))
    if missing:
        raise ValueError(f"GPS input missing required columns: {missing}")
    if radius_m <= 0:
        raise ValueError("radius_m must be positive")
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    store_records = _prepare_stores(stores)
    store_ids = [x[0] for x in store_records]
    store_lats = [x[1] for x in store_records]
    store_lons = [x[2] for x in store_records]

    for start in range(0, len(gps), chunk_size):
        subset = gps.iloc[start:start + chunk_size]
        output_rows = []
        for _, ping in subset.iterrows():
            lat = pd.to_numeric(ping["Latitude"], errors="coerce")
            lon = pd.to_numeric(ping["Longitude"], errors="coerce")
            if pd.isna(lat) or pd.isna(lon) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
                raise ValueError(f"Invalid GPS coordinates at row {ping.name}")
            _, _, distances = _GEOD.inv(
                [float(lon)] * len(store_records), [float(lat)] * len(store_records),
                store_lons, store_lats,
            )
            matches = [i for i, dist in enumerate(distances) if dist <= radius_m]
            if matches:
                for i in matches:
                    output_rows.append({
                        "DeviceID": ping["DeviceID"], "Store_ID": store_ids[i],
                        "Timestamp": ping["Timestamp"], "Inside_Catchment": True,
                        "Distance_Meters": float(distances[i]),
                    })
            else:
                i = min(range(len(distances)), key=lambda j: distances[j])
                output_rows.append({
                    "DeviceID": ping["DeviceID"], "Store_ID": store_ids[i],
                    "Timestamp": ping["Timestamp"], "Inside_Catchment": False,
                    "Distance_Meters": float(distances[i]),
                })
        chunk = pd.DataFrame(output_rows, columns=OUTPUT_COLUMNS)
        if not chunk.empty:
            chunk["Inside_Catchment"] = chunk["Inside_Catchment"].astype(bool)
            chunk["Distance_Meters"] = chunk["Distance_Meters"].astype(float)
        yield chunk


def spatial_join_gps_to_stores(gps, stores, radius_m=500):
    """Return the baseline spatial join for a complete input DataFrame."""
    chunks = list(spatial_join_chunks(gps, stores, radius_m=radius_m, chunk_size=max(1, len(gps))))
    if not chunks:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.concat(chunks, ignore_index=True)


def write_spatial_join_csv(result, output_path):
    """Write standardized output CSV without DataFrame index."""
    missing = sorted(set(OUTPUT_COLUMNS) - set(result.columns))
    if missing:
        raise ValueError(f"Spatial join output missing columns: {missing}")
    result.loc[:, OUTPUT_COLUMNS].to_csv(output_path, index=False)


def write_spatial_join_chunks_csv(gps, stores, output_path, radius_m=500, chunk_size=1000):
    """Stream join chunks into a CSV file to avoid holding the full output in memory."""
    first = True
    for chunk in spatial_join_chunks(gps, stores, radius_m=radius_m, chunk_size=chunk_size):
        chunk.to_csv(output_path, mode="w" if first else "a", header=first, index=False)
        first = False
    if first:
        pd.DataFrame(columns=OUTPUT_COLUMNS).to_csv(output_path, index=False)
