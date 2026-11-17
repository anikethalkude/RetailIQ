
-- ==========================================
-- RETAILIQ: BUSINESS INTELLIGENCE ANALYSIS
-- ==========================================


-- QUERY 1: Total business performance

SELECT
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE order_status = 'delivered'
    ) AS delivered_orders,
    ROUND(
        SUM(total_payment)::numeric, 2
    ) AS total_payment_value
FROM fact_orders;


-- QUERY 2: Monthly revenue trend

SELECT
    DATE_TRUNC(
        'month', order_purchase_timestamp
    )::date AS sales_month,

    COUNT(*) AS total_orders,

    ROUND(
        SUM(total_payment)::numeric, 2
    ) AS monthly_payment_value

FROM fact_orders

WHERE order_status = 'delivered'
  AND order_purchase_timestamp IS NOT NULL

GROUP BY 1
ORDER BY 1;


-- QUERY 3: Top 10 product categories by revenue

SELECT
    product_category_name_english AS category,

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(
        SUM(price)::numeric, 2
    ) AS product_revenue

FROM fact_order_items

WHERE order_status = 'delivered'

GROUP BY product_category_name_english

ORDER BY product_revenue DESC

LIMIT 10;


-- QUERY 4: Top 10 customer states by revenue

SELECT
    customer_state,

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(
        SUM(price)::numeric, 2
    ) AS product_revenue

FROM fact_order_items

WHERE order_status = 'delivered'

GROUP BY customer_state

ORDER BY product_revenue DESC

LIMIT 10;


-- QUERY 5: Repeat customer analysis

WITH customer_orders AS (

    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count

    FROM fact_order_items

    WHERE order_status = 'delivered'

    GROUP BY customer_unique_id
)

SELECT
    COUNT(*) AS unique_customers,

    COUNT(*) FILTER (
        WHERE order_count = 1
    ) AS one_time_customers,

    COUNT(*) FILTER (
        WHERE order_count > 1
    ) AS repeat_customers,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_count > 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage

FROM customer_orders;


-- QUERY 6: Monthly category performance
-- Using a window function to rank categories
-- within each month.

WITH category_ranking AS (

    SELECT
        purchase_month,
        product_category_name_english,
        SUM(revenue) AS category_revenue,

        RANK() OVER (
            PARTITION BY purchase_month
            ORDER BY SUM(revenue) DESC
        ) AS category_rank

    FROM monthly_category_demand

    GROUP BY
        purchase_month,
        product_category_name_english
)

SELECT *
FROM category_ranking

WHERE category_rank <= 3

ORDER BY purchase_month, category_rank;


-- QUERY 7: Delivery performance

SELECT
    COUNT(*) AS delivered_orders,

    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date
                    - order_purchase_timestamp
                )
            ) / 86400
        )::numeric, 2
    ) AS average_delivery_days,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date
              <= order_estimated_delivery_date
    ) AS on_time_deliveries,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date
              > order_estimated_delivery_date
    ) AS late_deliveries

FROM fact_orders

WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_purchase_timestamp IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;


-- ==========================================
-- END OF RETAILIQ SQL ANALYSIS
-- ==========================================
