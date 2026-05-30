-- Dashboard queries aligned to the customer-level churn dataset.
-- These power: churn drivers, cohort-style retention matrix, churn risk list, and growth lever scenarios.

-- 1) Overall KPI summary
SELECT
  COUNT(*) AS customers,
  AVG(Churn) AS churn_rate,
  AVG(Tenure) AS avg_tenure,
  AVG(OrderCount) AS avg_order_count,
  AVG(CashbackAmount) AS avg_cashback,
  AVG(Complain) AS complaint_rate
FROM ecomm_customers;

-- 2) Churn drivers (segment cuts)
-- Churn by complaint flag
SELECT
  Complain,
  COUNT(*) AS customers,
  AVG(Churn) AS churn_rate,
  AVG(SatisfactionScore) AS avg_satisfaction,
  AVG(DaySinceLastOrder) AS avg_days_since_last
FROM ecomm_customers
GROUP BY Complain
ORDER BY Complain;

-- Churn by payment mode
SELECT
  PreferredPaymentMode,
  COUNT(*) AS customers,
  AVG(Churn) AS churn_rate
FROM ecomm_customers
GROUP BY PreferredPaymentMode
ORDER BY churn_rate DESC;

-- Churn by preferred login device
SELECT
  PreferredLoginDevice,
  COUNT(*) AS customers,
  AVG(Churn) AS churn_rate
FROM ecomm_customers
GROUP BY PreferredLoginDevice
ORDER BY churn_rate DESC;

-- 3) Cohort-style retention heatmap (Tenure band x Recency band)
-- Retention proxy = 1 - churn_rate within each cell.
WITH base AS (
  SELECT
    CASE
      WHEN Tenure IS NULL THEN 'Unknown'
      WHEN Tenure <= 3 THEN '0-3'
      WHEN Tenure <= 6 THEN '4-6'
      WHEN Tenure <= 12 THEN '7-12'
      WHEN Tenure <= 24 THEN '13-24'
      ELSE '25+'
    END AS tenure_band,
    CASE
      WHEN DaySinceLastOrder IS NULL THEN 'Unknown'
      WHEN DaySinceLastOrder <= 7 THEN '0-7'
      WHEN DaySinceLastOrder <= 15 THEN '8-15'
      WHEN DaySinceLastOrder <= 30 THEN '16-30'
      ELSE '31+'
    END AS recency_band,
    Churn
  FROM ecomm_customers
)
SELECT
  tenure_band,
  recency_band,
  COUNT(*) AS customers,
  AVG(Churn) AS churn_rate,
  (1.0 - AVG(Churn)) AS retention_proxy
FROM base
GROUP BY tenure_band, recency_band
ORDER BY tenure_band, recency_band;

-- 4) Top churn-risk customers (rule-based RAG list)
-- In production you'd use the ML churn probability; this provides a SQL-only version.
SELECT
  CustomerID,
  Churn,
  Tenure,
  OrderCount,
  DaySinceLastOrder,
  SatisfactionScore,
  Complain,
  CashbackAmount,
  CASE
    WHEN (Complain = 1 AND DaySinceLastOrder >= 15) OR (DaySinceLastOrder >= 30) THEN 'Red'
    WHEN (DaySinceLastOrder BETWEEN 15 AND 29) OR (SatisfactionScore <= 2) THEN 'Amber'
    ELSE 'Green'
  END AS RAG_Status
FROM ecomm_customers
ORDER BY
  CASE
    WHEN RAG_Status = 'Red' THEN 1
    WHEN RAG_Status = 'Amber' THEN 2
    ELSE 3
  END,
  DaySinceLastOrder DESC;
