{% macro safe_divide(numerator, denominator) %}
    {#
        Returns numerator / denominator, or null instead of raising a
        divide-by-zero error when the denominator is 0. DuckDB already
        returns null for float division by zero, but this macro keeps the
        intent explicit and makes the project portable to warehouses
        (e.g. Snowflake, Postgres) that don't.
    #}
    case
        when {{ denominator }} = 0 or {{ denominator }} is null then null
        else {{ numerator }} / {{ denominator }}
    end
{% endmacro %}
