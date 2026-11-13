with source as (
    select * from {{ ref('raw_products') }}
),

renamed as (
    select
        product_id,
        product_name,
        category,
        unit_cost,
        unit_price,
        round(unit_price - unit_cost, 2) as unit_margin,
        round((unit_price - unit_cost) / unit_price, 4) as margin_pct,
        cast(is_active as boolean) as is_active
    from source
)

select * from renamed
