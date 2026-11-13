with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_revenue as (
    select
        orders.customer_id,
        orders.order_id,
        orders.is_completed,
        sum(order_items.line_item_revenue) as order_revenue
    from orders
    left join order_items on orders.order_id = order_items.order_id
    group by 1, 2, 3
),

customer_agg as (
    select
        customer_id,
        count(order_id) as lifetime_order_count,
        sum(case when is_completed then order_revenue else 0 end) as lifetime_revenue,
        min(case when is_completed then order_revenue end) as smallest_completed_order,
        max(case when is_completed then order_revenue end) as largest_completed_order
    from order_revenue
    group by 1
)

select
    customers.customer_id,
    customers.customer_name,
    customers.email,
    customers.state,
    customers.signup_date,
    customers.marketing_channel,
    coalesce(customer_agg.lifetime_order_count, 0) as lifetime_order_count,
    coalesce(customer_agg.lifetime_revenue, 0) as lifetime_revenue,
    customer_agg.largest_completed_order,
    case
        when coalesce(customer_agg.lifetime_revenue, 0) >= 500 then 'high_value'
        when coalesce(customer_agg.lifetime_revenue, 0) >= 150 then 'mid_value'
        when coalesce(customer_agg.lifetime_revenue, 0) > 0 then 'low_value'
        else 'no_purchases'
    end as customer_value_segment
from customers
left join customer_agg on customers.customer_id = customer_agg.customer_id
