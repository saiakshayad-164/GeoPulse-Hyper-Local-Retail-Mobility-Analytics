{{
    config(
        materialized='view'
    )
}}

with pings as (
    select * from {{ ref('stg_gps_pings') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
)

select
    p.device_id,
    s.store_id,
    p.ping_timestamp as match_timestamp,
    st_distance(p.gps_location, s.store_location) as distance_meters,
    case
        when st_distance(p.gps_location, s.store_location) <= 500 then true
        else false
    end as inside_catchment
from pings p
cross join stores s
where st_distance(p.gps_location, s.store_location) <= 500