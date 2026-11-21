{{
    config(
        materialized='table'
    )
}}

with stores as (
    select * from {{ ref('stg_stores') }}
),

spatial_matches as (
    select * from {{ ref('stg_spatial_matches') }}
)

select
    s.store_id,
    s.store_name,
    s.store_type,
    count(distinct sm.device_id) as overlapping_visitors
from stores s
left join spatial_matches sm on s.store_id = sm.store_id
group by 1, 2, 3