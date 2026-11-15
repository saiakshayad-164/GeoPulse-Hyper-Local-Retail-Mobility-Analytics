{{
    config(
        materialized='view'
    )
}}

with raw_stores as (
    select * from {{ source('geopulse_raw', 'dim_stores') }}
),

cleaned_stores as (
    select
        store_id,
        trim(store_name) as store_name,
        upper(trim(brand_type)) as brand_type,
        cast(latitude as float) as latitude,
        cast(longitude as float) as longitude,
        st_point(cast(longitude as float), cast(latitude as float)) as store_geo_point
    from raw_stores
    where latitude is not null
      and longitude is not null
      and store_id is not null
)

select * from cleaned_stores