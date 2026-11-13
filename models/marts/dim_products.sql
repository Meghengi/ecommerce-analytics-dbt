with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

completed_items as (
    select order_items.*
    from order_items
    inner join orders on order_items.order_id = orders.order_id
    where orders.is_completed
),

product_agg as (
    select
        product_id,
        sum(quantity) as units_sold,
        sum(line_item_revenue) as gross_revenue
    from completed_items
    group by 1
)

select
    products.product_id,
    products.product_name,
    products.category,
    products.unit_cost,
    products.unit_price,
    products.margin_pct,
    products.is_active,
    coalesce(product_agg.units_sold, 0) as units_sold,
    coalesce(product_agg.gross_revenue, 0) as gross_revenue
from products
left join product_agg on products.product_id = product_agg.product_id
