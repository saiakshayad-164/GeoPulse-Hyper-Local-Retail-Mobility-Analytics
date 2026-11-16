{{
    config(
        materialized='table'
    )
}}

with pings as (
    select * from {{ ref('stg_gps_pings') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
),

store_pings_matched as (
    select
        s.store_id,
        s.store_name,
        s.brand_type,
        s.latitude as store_lat,
        s.longitude as store_lon,
        p.ping_id,
        p.device_id,
        p.ping_hour,
        p.hour_of_day,
        p.day_of_week,
        st_distance(s.store_geo_point, p.geo_point) as distance_meters
    from stores s
    inner join pings p
        on st_dwithin(s.store_geo_point, p.geo_point, 100)
),

hourly_footfall as (
    select
        store_id,
        store_name,
        brand_type,
        store_lat,
        store_lon,
        ping_hour,
        hour_of_day,
        day_of_week,
        count(distinct device_id) as unique_visitors,
        count(ping_id) as total_pings,
        round(avg(distance_meters), 2) as avg_proximity_meters
    from store_pings_matched
    group by 1, 2, 3, 4, 5, 6, 7, 8
)

select * from hourly_footfall