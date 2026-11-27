{{ config(materialized='table') }}

with pings as (
    select * from {{ ref('stg_gps_pings') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
),

-- Match GPS pings within 500m store catchment radius
matched_pings as (
    select
        p.device_id,
        s.store_id,
        s.store_name,
        s.store_lat,
        s.store_lon,
        p.ping_timestamp,
        date_trunc('hour', p.ping_timestamp) as visit_hour,
        extract(hour from p.ping_timestamp) as hour_of_day,
        round(
            6371000 * 2 * asin(sqrt(
                power(sin(radians((p.latitude - s.store_lat) / 2)), 2) +
                cos(radians(s.store_lat)) * cos(radians(p.latitude)) *
                power(sin(radians((p.longitude - s.store_lon) / 2)), 2)
            )), 2
        ) as distance_meters
    from pings p
    cross join stores s
    where 6371000 * 2 * asin(sqrt(
        power(sin(radians((p.latitude - s.store_lat) / 2)), 2) +
        cos(radians(s.store_lat)) * cos(radians(p.latitude)) *
        power(sin(radians((p.longitude - s.store_lon) / 2)), 2)
    )) <= 500
),

-- Deduplicate to one visit record per device per store per hour and rank visit sequence
device_store_visits as (
    select
        device_id,
        store_id,
        store_name,
        store_lat,
        store_lon,
        visit_hour,
        hour_of_day,
        min(ping_timestamp) as first_ping_at,
        max(ping_timestamp) as last_ping_at,
        count(*) as ping_count,
        round(avg(distance_meters), 2) as avg_distance_meters,
        row_number() over (
            partition by device_id
            order by min(ping_timestamp) asc
        ) as device_visit_seq
    from matched_pings
    group by
        device_id,
        store_id,
        store_name,
        store_lat,
        store_lon,
        visit_hour,
        hour_of_day
)

select * from device_store_visits