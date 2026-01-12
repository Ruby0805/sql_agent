-- Example Business SQL Queries for E-Commerce Database
-- These queries demonstrate common business analytics and reporting scenarios

-- ============================================================
-- SALES ANALYSIS
-- ============================================================

-- 1. Total revenue by month
SELECT
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as total_orders,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY month
ORDER BY month DESC;

-- 2. Top 10 best-selling products
SELECT
    p.product_name,
    p.sku,
    SUM(oi.quantity) as units_sold,
    SUM(oi.subtotal) as total_revenue,
    COUNT(DISTINCT oi.order_id) as number_of_orders
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status != 'Cancelled'
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Revenue by product category
SELECT
    c.category_name,
    COUNT(DISTINCT p.product_id) as product_count,
    SUM(oi.quantity) as units_sold,
    SUM(oi.subtotal) as total_revenue
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.category_id
ORDER BY total_revenue DESC;

-- ============================================================
-- CUSTOMER ANALYSIS
-- ============================================================

-- 4. Top 20 customers by total spend
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    c.loyalty_points
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 20;

-- 5. Customer retention - repeat customers
SELECT
    CASE
        WHEN order_count = 1 THEN '1 Order'
        WHEN order_count BETWEEN 2 AND 5 THEN '2-5 Orders'
        WHEN order_count BETWEEN 6 AND 10 THEN '6-10 Orders'
        ELSE '11+ Orders'
    END as customer_segment,
    COUNT(*) as customer_count,
    SUM(total_spent) as segment_revenue
FROM (
    SELECT
        c.customer_id,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'Cancelled'
    GROUP BY c.customer_id
)
GROUP BY customer_segment
ORDER BY
    CASE customer_segment
        WHEN '1 Order' THEN 1
        WHEN '2-5 Orders' THEN 2
        WHEN '6-10 Orders' THEN 3
        ELSE 4
    END;

-- 6. Customer geographic distribution
SELECT
    country,
    state,
    COUNT(DISTINCT customer_id) as customer_count,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'Cancelled'
GROUP BY country, state
HAVING customer_count > 5
ORDER BY total_revenue DESC;

-- ============================================================
-- INVENTORY MANAGEMENT
-- ============================================================

-- 7. Low stock alert - products below reorder level
SELECT
    p.product_name,
    p.sku,
    c.category_name,
    i.quantity_on_hand,
    i.reorder_level,
    i.warehouse_location,
    s.supplier_name,
    s.email as supplier_email
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE i.quantity_on_hand <= i.reorder_level
    AND p.is_active = 1
ORDER BY (i.reorder_level - i.quantity_on_hand) DESC;

-- 8. Inventory value by warehouse
SELECT
    i.warehouse_location,
    COUNT(DISTINCT p.product_id) as product_count,
    SUM(i.quantity_on_hand) as total_units,
    SUM(i.quantity_on_hand * p.cost_price) as inventory_value_cost,
    SUM(i.quantity_on_hand * p.unit_price) as inventory_value_retail
FROM inventory i
JOIN products p ON i.product_id = p.product_id
GROUP BY i.warehouse_location
ORDER BY inventory_value_retail DESC;

-- 9. Products with no recent sales (last 90 days)
SELECT
    p.product_id,
    p.product_name,
    p.sku,
    c.category_name,
    i.quantity_on_hand,
    p.unit_price,
    MAX(o.order_date) as last_order_date
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status != 'Cancelled'
WHERE p.is_active = 1
GROUP BY p.product_id
HAVING last_order_date IS NULL OR last_order_date < date('now', '-90 days')
ORDER BY i.quantity_on_hand DESC;

-- ============================================================
-- EMPLOYEE PERFORMANCE
-- ============================================================

-- 10. Sales by employee
SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name as employee_name,
    e.position,
    d.department_name,
    COUNT(o.order_id) as orders_processed,
    SUM(o.total_amount) as total_sales,
    AVG(o.total_amount) as avg_order_value
FROM employees e
JOIN departments d ON e.department_id = d.department_id
LEFT JOIN orders o ON e.employee_id = o.employee_id AND o.order_status != 'Cancelled'
WHERE e.is_active = 1
GROUP BY e.employee_id
HAVING orders_processed > 0
ORDER BY total_sales DESC;

-- 11. Department performance
SELECT
    d.department_name,
    COUNT(DISTINCT e.employee_id) as employee_count,
    AVG(e.salary) as avg_salary,
    SUM(e.salary) as total_payroll,
    d.budget,
    d.budget - SUM(e.salary) as budget_remaining
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id AND e.is_active = 1
GROUP BY d.department_id
ORDER BY total_payroll DESC;

-- ============================================================
-- PRODUCT ANALYSIS
-- ============================================================

-- 12. Products with highest profit margins
SELECT
    p.product_name,
    p.sku,
    c.category_name,
    p.cost_price,
    p.unit_price,
    (p.unit_price - p.cost_price) as profit_per_unit,
    ROUND(((p.unit_price - p.cost_price) / p.cost_price * 100), 2) as profit_margin_pct,
    SUM(oi.quantity) as units_sold,
    SUM((p.unit_price - p.cost_price) * oi.quantity) as total_profit
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status != 'Cancelled'
WHERE p.is_active = 1
GROUP BY p.product_id
HAVING units_sold > 0
ORDER BY profit_margin_pct DESC
LIMIT 20;

-- 13. Average product ratings by category
SELECT
    c.category_name,
    COUNT(DISTINCT p.product_id) as product_count,
    COUNT(pr.review_id) as total_reviews,
    ROUND(AVG(pr.rating), 2) as avg_rating,
    SUM(CASE WHEN pr.rating = 5 THEN 1 ELSE 0 END) as five_star_reviews,
    SUM(CASE WHEN pr.rating = 1 THEN 1 ELSE 0 END) as one_star_reviews
FROM categories c
JOIN products p ON c.category_id = p.category_id
LEFT JOIN product_reviews pr ON p.product_id = pr.product_id
GROUP BY c.category_id
HAVING total_reviews > 0
ORDER BY avg_rating DESC;

-- 14. Products with most reviews
SELECT
    p.product_name,
    p.sku,
    COUNT(pr.review_id) as review_count,
    ROUND(AVG(pr.rating), 2) as avg_rating,
    SUM(pr.helpful_count) as total_helpful_votes,
    SUM(oi.quantity) as units_sold
FROM products p
JOIN product_reviews pr ON p.product_id = pr.product_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status != 'Cancelled'
GROUP BY p.product_id
ORDER BY review_count DESC
LIMIT 15;

-- ============================================================
-- ORDER ANALYSIS
-- ============================================================

-- 15. Order status distribution
SELECT
    order_status,
    COUNT(*) as order_count,
    SUM(total_amount) as total_value,
    AVG(total_amount) as avg_order_value,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- 16. Average order processing time
SELECT
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as orders_shipped,
    ROUND(AVG(julianday(shipped_date) - julianday(order_date)), 2) as avg_days_to_ship,
    MIN(julianday(shipped_date) - julianday(order_date)) as min_days,
    MAX(julianday(shipped_date) - julianday(order_date)) as max_days
FROM orders
WHERE shipped_date IS NOT NULL
GROUP BY month
ORDER BY month DESC;

-- 17. Payment method analysis
SELECT
    payment_method,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_transaction,
    payment_status
FROM payments
GROUP BY payment_method, payment_status
ORDER BY total_amount DESC;

-- ============================================================
-- SHIPPING ANALYSIS
-- ============================================================

-- 18. Shipping carrier performance
SELECT
    s.carrier,
    COUNT(*) as shipments,
    AVG(s.shipping_cost) as avg_cost,
    ROUND(AVG(julianday(s.actual_delivery) - julianday(s.shipping_date)), 2) as avg_delivery_days,
    SUM(CASE WHEN s.actual_delivery <= s.estimated_delivery THEN 1 ELSE 0 END) as on_time_deliveries,
    ROUND(SUM(CASE WHEN s.actual_delivery <= s.estimated_delivery THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as on_time_pct
FROM shipping s
WHERE s.actual_delivery IS NOT NULL
GROUP BY s.carrier
ORDER BY on_time_pct DESC;

-- ============================================================
-- ADVANCED ANALYTICS
-- ============================================================

-- 19. Customer Lifetime Value (CLV) analysis
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.registration_date,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    AVG(o.total_amount) as avg_order_value,
    ROUND(julianday('now') - julianday(c.registration_date)) as days_as_customer,
    ROUND(SUM(o.total_amount) / (julianday('now') - julianday(c.registration_date)) * 365, 2) as annual_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'Cancelled'
WHERE c.is_active = 1
GROUP BY c.customer_id
HAVING total_orders > 0
ORDER BY lifetime_value DESC
LIMIT 25;

-- 20. Monthly sales growth rate
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_date) as month,
        SUM(total_amount) as revenue
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month_revenue,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY month)) /
           LAG(revenue) OVER (ORDER BY month) * 100), 2) as growth_rate_pct
FROM monthly_sales
ORDER BY month DESC;

-- 21. Customer churn analysis - customers who haven't ordered in 6 months
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.email,
    MAX(o.order_date) as last_order_date,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    ROUND(julianday('now') - julianday(MAX(o.order_date))) as days_since_last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'Cancelled'
WHERE c.is_active = 1
GROUP BY c.customer_id
HAVING days_since_last_order > 180
ORDER BY lifetime_value DESC;

-- 22. Supplier performance analysis
SELECT
    s.supplier_name,
    s.country,
    s.rating,
    COUNT(DISTINCT p.product_id) as products_supplied,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.subtotal) as total_revenue_generated,
    ROUND(AVG(p.unit_price - p.cost_price), 2) as avg_profit_margin
FROM suppliers s
JOIN products p ON s.supplier_id = p.supplier_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status != 'Cancelled'
GROUP BY s.supplier_id
ORDER BY total_revenue_generated DESC;

-- 23. Promotion effectiveness
SELECT
    p.promotion_name,
    p.promotion_code,
    p.discount_type,
    p.discount_value,
    p.start_date,
    p.end_date,
    p.times_used,
    p.usage_limit,
    ROUND(p.times_used * 100.0 / p.usage_limit, 2) as usage_rate_pct,
    p.is_active
FROM promotions p
ORDER BY p.times_used DESC;

-- 24. ABC Analysis - Product classification by revenue
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(oi.subtotal) as total_revenue,
        SUM(SUM(oi.subtotal)) OVER () as grand_total
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status != 'Cancelled'
    GROUP BY p.product_id
),
product_percentages AS (
    SELECT
        product_id,
        product_name,
        total_revenue,
        ROUND(total_revenue * 100.0 / grand_total, 2) as revenue_pct,
        SUM(total_revenue * 100.0 / grand_total) OVER (ORDER BY total_revenue DESC) as cumulative_pct
    FROM product_revenue
)
SELECT
    product_name,
    total_revenue,
    revenue_pct,
    ROUND(cumulative_pct, 2) as cumulative_pct,
    CASE
        WHEN cumulative_pct <= 70 THEN 'A - High Value'
        WHEN cumulative_pct <= 90 THEN 'B - Medium Value'
        ELSE 'C - Low Value'
    END as abc_classification
FROM product_percentages
ORDER BY total_revenue DESC;

-- 25. Cohort analysis - Customer retention by registration month
WITH customer_cohorts AS (
    SELECT
        c.customer_id,
        strftime('%Y-%m', c.registration_date) as cohort_month,
        strftime('%Y-%m', o.order_date) as order_month
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'Cancelled'
)
SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) as cohort_size,
    COUNT(DISTINCT CASE WHEN order_month = cohort_month THEN customer_id END) as month_0,
    COUNT(DISTINCT CASE WHEN order_month = date(cohort_month || '-01', '+1 month', 'start of month') THEN customer_id END) as month_1,
    COUNT(DISTINCT CASE WHEN order_month = date(cohort_month || '-01', '+2 month', 'start of month') THEN customer_id END) as month_2
FROM customer_cohorts
GROUP BY cohort_month
ORDER BY cohort_month DESC
LIMIT 12;
