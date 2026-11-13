with source as (
    select * from {{ ref('raw_order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price_at_purchase,
        round(quantity * unit_price_at_purchase, 2) as line_item_revenue
    from source
)

select * from renamed
