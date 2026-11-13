with fct as (
    select * from {{ ref('fct_order_items') }}
    where is_completed
),

monthly as (
    select
        date_trunc('month', order_date) as order_month,
        category,
        count(distinct order_id) as completed_orders,
        sum(quantity) as units_sold,
        sum(line_item_revenue) as gross_revenue,
        sum(line_item_margin) as gross_margin
    from fct
    group by 1, 2
)

select
    order_month,
    category,
    completed_orders,
    units_sold,
    gross_revenue,
    gross_margin,
    round({{ safe_divide('gross_margin', 'gross_revenue') }}, 4) as margin_pct
from monthly
order by order_month, category
