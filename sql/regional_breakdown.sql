-- =============================================================
-- SalesFlow — Regional Breakdown (Gender & Age Segment)
-- =============================================================
-- Business Question: How does sales performance vary by customer segment?
-- Note: Dataset has no region column, so we segment by gender + age_group
-- Used in: Streamlit segment breakdown, Power BI demographic visual
-- =============================================================

-- Breakdown by Gender
SELECT
    'gender' AS segment_type,
    gender AS segment_value,
    COUNT(transaction_id) AS total_transactions,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    SUM(quantity)  AS total_units_sold,
    ROUND(
        SUM(total_amount) * 100.0 /
        SUM(SUM(total_amount)) OVER (), 2
    )                                       AS revenue_share_pct
FROM
    sales
GROUP BY
    gender

UNION ALL

-- Breakdown by Age Group
SELECT
    'age_group' AS segment_type,
    age_group AS segment_value,
    COUNT(transaction_id) AS total_transactions,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    SUM(quantity) AS total_units_sold,
    ROUND(
        SUM(total_amount) * 100.0 /
        SUM(SUM(total_amount)) OVER (), 2
    )                                       AS revenue_share_pct
FROM
    sales
GROUP BY
    age_group

ORDER BY
    segment_type, total_revenue DESC;