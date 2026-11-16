{{
    config(
        materialized='table'
    )
}}

with own_stores as (
    select * from {{ ref('stg_stores') }}
    where brand_type = 'OWN'
),

all_stores as (
    select * from {{ ref('stg_stores') }}
),

store_pairs as (
    select
        o.store_id as target_store_id,
        o.store_name as target_store_name,
        o.latitude as target_lat,
        o.longitude as target_lon,
        a.store_id as nearby_store_id,
        a.store_name as nearby_store_name,
        a.brand_type as nearby_brand_type,
        round(st_distance(o.store_geo_point, a.store_geo_point), 2) as distance_meters
    from own_stores o
    inner join all_stores a
        on o.store_id != a.store_id
        and st_dwithin(o.store_geo_point, a.store_geo_point, 2000)
),

cannibalization_risk as (
    select
        target_store_id,
        target_store_name,
        target_lat,
        target_lon,
        nearby_store_id,
        nearby_store_name,
        nearby_brand_type,
        distance_meters,
        case
            when distance_meters <= 500 then 'HIGH'
            when distance_meters <= 1000 then 'MEDIUM'
            else 'LOW'
        end as overlap_risk_level
    from store_pairs
)

select * from cannibalization_risk