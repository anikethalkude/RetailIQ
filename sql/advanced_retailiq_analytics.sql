
-- =====================================================
-- RETAILIQ
-- ADVANCED RETAIL ANALYTICS
-- =====================================================

-- QUERY 1: MONTH-OVER-MONTH REVENUE GROWTH
-- Calculates monthly revenue and percentage growth.

WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_purchase_timestamp) AS month,
        SUM(total_payment) AS revenue
    FROM public.fact_orders
    WHERE order_status = 'delivered'
    GROUP BY 1
),
revenue_comparison AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS previous_revenue
    FROM monthly_revenue
)
SELECT
    month,
    ROUND(revenue::numeric, 2) AS monthly_revenue,
    ROUND(previous_revenue::numeric, 2) AS previous_revenue,
    ROUND(
        (
            (revenue - previous_revenue)
            / NULLIF(previous_revenue, 0) * 100
        )::numeric,
        2
    ) AS growth_percentage
FROM revenue_comparison
ORDER BY month;


-- =====================================================
-- QUERY 2: TOP 10 PRODUCT CATEGORIES
-- Identifies categories with highest product revenue.
-- =====================================================

SELECT
    product_category_name_english AS category,
    SUM(order_item_count) AS total_demand,
    ROUND(SUM(revenue)::numeric, 2) AS total_revenue
FROM public.monthly_category_demand
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;


-- =====================================================
-- QUERY 3: CATEGORY REVENUE CONTRIBUTION
-- Calculates each category's share of total revenue.
-- =====================================================

WITH category_revenue AS (
    SELECT
        product_category_name_english AS category,
        SUM(revenue) AS revenue
    FROM public.monthly_category_demand
    GROUP BY product_category_name_english
)
SELECT
    category,
    ROUND(revenue::numeric, 2) AS category_revenue,
    ROUND(
        (
            revenue / NULLIF(SUM(revenue) OVER (), 0) * 100
        )::numeric,
        2
    ) AS revenue_contribution_percentage
FROM category_revenue
ORDER BY revenue DESC;


-- =====================================================
-- QUERY 4: FORECAST MODEL PERFORMANCE
-- Compares Baseline and Random Forest MAE.
-- Lower MAE indicates better performance.
-- =====================================================

SELECT
    category,
    ROUND(baseline_mae::numeric, 2) AS baseline_mae,
    ROUND(random_forest_mae::numeric, 2)
        AS random_forest_mae,
    CASE
        WHEN baseline_mae < random_forest_mae
            THEN 'Baseline'
        WHEN random_forest_mae < baseline_mae
            THEN 'Random Forest'
        ELSE 'Equal Performance'
    END AS better_model
FROM public.forecast_metrics
ORDER BY LEAST(baseline_mae, random_forest_mae);


-- =====================================================
-- QUERY 5: FUTURE DEMAND RANKING
-- Ranks categories by total predicted demand.
-- =====================================================

SELECT
    category,
    ROUND(SUM(predicted_demand)::numeric, 2)
        AS total_predicted_demand,
    RANK() OVER (
        ORDER BY SUM(predicted_demand) DESC
    ) AS demand_rank
FROM public.future_demand_forecast
GROUP BY category
ORDER BY demand_rank;


-- =====================================================
-- END OF RETAILIQ ADVANCED SQL ANALYTICS
-- =====================================================
