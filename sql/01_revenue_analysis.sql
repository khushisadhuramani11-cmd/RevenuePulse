
USE revenuepulse;

-- 1. Overall business performance
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2
    ) AS profit_margin_pct
FROM sales;


-- 2. Monthly revenue and profit
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2
    ) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;


-- 3. Month-over-month revenue growth
WITH monthly AS (
    SELECT
        CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month_start,
        SUM(sales) AS revenue
    FROM sales
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
growth AS (
    SELECT
        month_start,
        revenue,
        LAG(revenue) OVER (ORDER BY month_start) AS previous_revenue
    FROM monthly
)
SELECT
    month_start,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        100.0 * (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0), 2
    ) AS mom_growth_pct
FROM growth
ORDER BY month_start;


-- 4. Category-wise performance
SELECT
    category,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2
    ) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY category
ORDER BY revenue DESC;


-- 5. Sub-category profitability
SELECT
    category,
    `sub-category` AS sub_category,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2
    ) AS profit_margin_pct
FROM sales
GROUP BY category, `sub-category`
ORDER BY profit ASC;


-- 6. Regional performance
SELECT
    region,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2
    ) AS profit_margin_pct
FROM sales
GROUP BY region
ORDER BY revenue DESC;


-- 7. Customer segment performance
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM sales
GROUP BY segment
ORDER BY revenue DESC;


-- 8. Discount and profitability analysis
SELECT
    discount,
    COUNT(*) AS record_count,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(AVG(profit), 2) AS average_profit
FROM sales
GROUP BY discount
ORDER BY discount;
