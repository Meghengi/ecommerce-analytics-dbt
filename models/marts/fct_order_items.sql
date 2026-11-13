{{
    config(
        materialized='table'
    )
}}

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    order_items.order_item_id,
    order_items.order_id,
    orders.customer_id,
    orders.order_date,
    orders.status,
    orders.is_completed,
    order_items.product_id,
    products.category,
    order_items.quantity,
    order_items.unit_price_at_purchase,
    order_items.line_item_revenue,
    round(order_items.quantity * products.unit_cost, 2) as line_item_cost,
    round(order_items.line_item_revenue - (order_items.quantity * products.unit_cost), 2) as line_item_margin
from order_items
inner join orders on order_items.order_id = orders.order_id
inner join products on order_items.product_id = products.product_id
