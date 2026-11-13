with source as (
    select * from {{ ref('raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as customer_name,
        lower(email) as email,
        state,
        signup_date,
        marketing_channel
    from source
)

select * from renamed
