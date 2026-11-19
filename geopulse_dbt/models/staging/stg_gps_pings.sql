{{
    config(
        materialized='view'
    )
}}

with source_data as (
    select * from {{ source('geopulse_raw', 'GPS_PINGS') }}
),

cleaned as (
    select
        cast(DEVICEID as varchar) as device_id,
        cast(LATITUDE as float) as latitude,
        cast(LONGITUDE as float) as longitude,
        cast(EVENT_TIMESTAMP as timestamp_ntz) as ping_timestamp,
        LOCATION as gps_location
    from source_data
    where DEVICEID is not null
      and LATITUDE is not null
      and LONGITUDE is not null
      and EVENT_TIMESTAMP is not null
)

select distinct * from cleaned