-- Singular test: a completed order's line-item margin should never be
-- negative in this dataset (unit_price > unit_cost is guaranteed at data
-- generation time). dbt fails this test if it returns any rows.

select *
from {{ ref('fct_order_items') }}
where is_completed
  and line_item_margin < 0
