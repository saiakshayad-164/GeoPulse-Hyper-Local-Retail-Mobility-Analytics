{{
    config(
        materialized='view'
    )
}}

with source_data as (
    select * from {{ source('geopulse_raw', 'STORE_MASTER') }}
),

cleaned as (
    select
        cast(STORE_ID as varchar) as store_id,
        trim(STORE_NAME) as store_name,
        cast(LATITUDE as float) as store_lat,
        cast(LONGITUDE as float) as store_lon,
        trim(AREA) as area,
        trim(STORE_TYPE) as store_type,
        LOCATION as store_location
    from source_data
    where STORE_ID is not null
      and LATITUDE is not null
      and LONGITUDE is not null
)

select distinct * from cleaned