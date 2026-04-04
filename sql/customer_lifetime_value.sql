-- =============================================================
-- SalesFlow — Customer Lifetime Value (CLV)
-- =============================================================
-- Business Question: What is the total and average spend per customer?
-- Used in: Streamlit CLV table, Power BI customer segment visual
-- =============================================================

SELECT
    customer_id,
    gender,
    age,
    age_group,
    COUNT(transaction_id)               AS total_transactions,
    SUM(total_amount)                   AS lifetime_value,
    ROUND(AVG(total_amount), 2)         AS avg_order_value,
    SUM(quantity)                       AS total_units_purchased,
    MIN(date)                           AS first_purchase_date,
    MAX(date)                           AS last_purchase_date
FROM
    sales
GROUP BY
    customer_id, gender, age, age_group
ORDER BY
    lifetime_value DESC;