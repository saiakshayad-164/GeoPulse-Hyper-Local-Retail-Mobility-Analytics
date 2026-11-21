{{
    config(
        materialized='table'
    )
}}

with spatial_matches as (
    select * from {{ ref('stg_spatial_matches') }}
    where inside_catchment = true
),

stores as (
    select * from {{ ref('stg_stores') }}
),

hourly_footfall as (
    select
        m.store_id,
        s.store_name,
        s.store_lat,
        s.store_lon,
        date_trunc('hour', m.match_timestamp) as hour,
        extract(hour from m.match_timestamp) as hour_of_day,
        case
            when extract(hour from m.match_timestamp) between 6 and 11 then 'Morning'
            when extract(hour from m.match_timestamp) between 12 and 17 then 'Afternoon'
            when extract(hour from m.match_timestamp) between 18 and 22 then 'Evening'
            else 'Night'
        end as time_period_label,
        count(distinct m.device_id) as unique_visitors,
        count(*) as total_pings,
        round(avg(m.distance_meters), 2) as avg_distance_meters
    from spatial_matches m
    left join stores s
        on m.store_id = s.store_id
    group by 1, 2, 3, 4, 5, 6, 7
)

select * from hourly_footfall