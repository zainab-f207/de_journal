SELECT
    order_id,
    customer_name,
    amount::NUMERIC AS amount,
    CASE
        WHEN amount::NUMERIC > 100 THEN 'High order value'
        WHEN amount::NUMERIC >= 20 THEN 'Medium order value'
        ELSE 'Low order value'
    END AS classification
FROM {{ source('raw', 'raw_data') }}
WHERE amount ~ '^[0-9]+\.?[0-9]*$'