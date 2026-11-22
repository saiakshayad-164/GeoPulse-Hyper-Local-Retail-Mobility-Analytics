"""Build metric store catchment polygons for GeoPulse."""
import pandas as pd
from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.ops import transform


def build_store_catchments(stores, radius_m=500, resolution=32):
    """Return store rows with circular catchments in WGS84 geometry.

    Each store is buffered in a local azimuthal-equidistant CRS centered on
    that store, so the radius is expressed in meters rather than degrees.
    """
    required = {"Store_ID", "Store_Name", "Latitude", "Longitude"}
    missing = sorted(required - set(stores.columns))
    if missing:
        raise ValueError(f"Store input missing required columns: {missing}")
    if radius_m <= 0:
        raise ValueError("radius_m must be positive")
    if resolution < 1:
        raise ValueError("resolution must be at least 1")

    records = []
    for _, row in stores.iterrows():
        lat = pd.to_numeric(row["Latitude"], errors="coerce")
        lon = pd.to_numeric(row["Longitude"], errors="coerce")
        if pd.isna(lat) or pd.isna(lon) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(f"Invalid coordinates for store {row['Store_ID']}")
        local_crs = CRS.from_proj4(
            f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs"
        )
        forward = Transformer.from_crs("EPSG:4326", local_crs, always_xy=True).transform
        inverse = Transformer.from_crs(local_crs, "EPSG:4326", always_xy=True).transform
        point = transform(forward, Point(float(lon), float(lat)))
        polygon_wgs84 = transform(inverse, point.buffer(radius_m, resolution=resolution))
        records.append({
            "Store_ID": row["Store_ID"],
            "Store_Name": row["Store_Name"],
            "Latitude": float(lat),
            "Longitude": float(lon),
            "Radius_Meters": float(radius_m),
            "geometry": polygon_wgs84,
        })
    return pd.DataFrame(records, columns=[
        "Store_ID", "Store_Name", "Latitude", "Longitude", "Radius_Meters", "geometry"
    ])
