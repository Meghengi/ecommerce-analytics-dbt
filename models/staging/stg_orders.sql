with source as (
    select * from {{ ref('raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        shipping_cost,
        case when status = 'completed' then true else false end as is_completed
    from source
)

select * from renamed
