-- Cohort retention query (PostgreSQL syntax)
WITH first_purchase AS (
  SELECT
    o.user_id,
    MIN(o.order_date) AS first_order_date,
    DATE_TRUNC('month', MIN(o.order_date)) AS cohort_month
  FROM orders o
  GROUP BY o.user_id
),
orders_ext AS (
  SELECT
    o.user_id,
    o.order_id,
    DATE_TRUNC('month', o.order_date) AS order_month
  FROM orders o
),
cohort_index AS (
  SELECT
    e.user_id,
    f.cohort_month,
    e.order_month,
    EXTRACT(YEAR FROM e.order_month) * 12 + EXTRACT(MONTH FROM e.order_month)
    - (EXTRACT(YEAR FROM f.cohort_month) * 12 + EXTRACT(MONTH FROM f.cohort_month)) AS month_index
  FROM orders_ext e
  JOIN first_purchase f USING(user_id)
),
cohort_size AS (
  SELECT cohort_month, COUNT(*) AS cohort_size
  FROM first_purchase
  GROUP BY cohort_month
),
retention AS (
  SELECT
    c.cohort_month,
    c.month_index,
    COUNT(DISTINCT c.user_id) AS active_users
  FROM cohort_index c
  GROUP BY c.cohort_month, c.month_index
)
SELECT
  r.cohort_month,
  r.month_index,
  cs.cohort_size,
  r.active_users,
  ROUND(r.active_users::NUMERIC / NULLIF(cs.cohort_size, 0) * 100, 1) AS retention_pct
FROM retention r
JOIN cohort_size cs USING (cohort_month)
ORDER BY r.cohort_month, r.month_index;
