"""Input validation helpers for GeoPulse geospatial processing.

These dependency-free checks run before coordinates are converted into Sedona
geometries, so malformed input can be reported with a clear error message.
"""

from math import isfinite
from numbers import Real
from typing import Iterable


def validate_coordinate(latitude: object, longitude: object) -> tuple[float, float]:
    """Validate one WGS84 coordinate and return (latitude, longitude).

    Latitude must be within [-90, 90] and longitude within [-180, 180].
    Numeric strings are deliberately not coerced; ingestion should parse data
    types explicitly rather than silently accepting inconsistent source data.
    """
    if isinstance(latitude, bool) or not isinstance(latitude, Real):
        raise ValueError("Latitude must be a numeric value.")
    if isinstance(longitude, bool) or not isinstance(longitude, Real):
        raise ValueError("Longitude must be a numeric value.")

    lat = float(latitude)
    lon = float(longitude)
    if not isfinite(lat) or not -90.0 <= lat <= 90.0:
        raise ValueError(f"Latitude must be finite and between -90 and 90; got {latitude!r}.")
    if not isfinite(lon) or not -180.0 <= lon <= 180.0:
        raise ValueError(f"Longitude must be finite and between -180 and 180; got {longitude!r}.")
    return lat, lon


def validate_positive_radius(radius_m: object) -> float:
    """Return a positive finite catchment radius in metres."""
    if isinstance(radius_m, bool) or not isinstance(radius_m, Real):
        raise ValueError("Catchment radius must be a numeric value in metres.")

    radius = float(radius_m)
    if not isfinite(radius) or radius <= 0:
        raise ValueError(f"Catchment radius must be finite and greater than zero; got {radius_m!r}.")
    return radius


def validate_required_columns(
    actual_columns: Iterable[str],
    required_columns: Iterable[str],
    dataset_name: str = "Input",
) -> None:
    """Raise a useful error when a dataset is missing required columns."""
    actual = set(actual_columns)
    required = set(required_columns)
    missing = sorted(required - actual)
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"{dataset_name} is missing required column(s): {missing_text}.")


if __name__ == "__main__":
    # Quick local smoke check: python akshaya/src/input_validation.py
    assert validate_coordinate(17.3850, 78.4867) == (17.385, 78.4867)
    assert validate_positive_radius(500) == 500.0
    validate_required_columns(
        ["DeviceID", "Latitude", "Longitude", "Timestamp"],
        ["DeviceID", "Latitude", "Longitude", "Timestamp"],
        "GPS pings",
    )
    print("GeoPulse input validation checks passed.")
