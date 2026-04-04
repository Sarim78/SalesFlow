-- =============================================================
-- SalesFlow — Top Products by Revenue
-- =============================================================
-- Business Question: Which product categories drive the most revenue?
-- Used in: Streamlit bar chart, Power BI top categories visual
-- =============================================================

SELECT
    product_category,
    COUNT(transaction_id) AS total_transactions,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    SUM(quantity) AS total_units_sold,
    ROUND(
        SUM(total_amount) * 100.0 /
        SUM(SUM(total_amount)) OVER (), 2
    )                                   AS revenue_share_pct
FROM
    sales
GROUP BY
    product_category
ORDER BY
    total_revenue DESC;