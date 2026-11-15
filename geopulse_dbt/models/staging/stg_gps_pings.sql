{{
    config(
        materialized='view'
    )
}}

with raw_pings as (
    select * from {{ source('geopulse_raw', 'raw_gps_pings') }}
),

cleaned_pings as (
    select
        ping_id,
        device_id,
        cast(latitude as float) as latitude,
        cast(longitude as float) as longitude,
        to_timestamp_ntz(ping_timestamp) as ping_timestamp,
        date_trunc('hour', to_timestamp_ntz(ping_timestamp)) as ping_hour,
        extract(hour from to_timestamp_ntz(ping_timestamp)) as hour_of_day,
        dayname(to_timestamp_ntz(ping_timestamp)) as day_of_week,
        st_point(cast(longitude as float), cast(latitude as float)) as geo_point
    from raw_pings
    where latitude is not null
      and longitude is not null
      and latitude between -90 and 90
      and longitude between -180 and 180
      and device_id is not null
    qualify row_number() over (
        partition by device_id, ping_timestamp 
        order by ping_id
    ) = 1
)

select * from cleaned_pings