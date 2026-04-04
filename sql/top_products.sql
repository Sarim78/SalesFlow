-- =============================================================
-- SalesFlow — Monthly Revenue Trends
-- =============================================================
-- Business Question: How has revenue trended month over month?
-- Used in: Streamlit line chart, Power BI revenue trend visual
-- =============================================================

SELECT
    month_year,
    year,
    month,
    COUNT(transaction_id)           AS total_transactions,
    SUM(total_amount)               AS total_revenue,
    ROUND(AVG(total_amount), 2)     AS avg_order_value,
    SUM(quantity)                   AS total_units_sold
FROM
    sales
GROUP BY
    month_year, year, month
ORDER BY
    year ASC, month ASC;