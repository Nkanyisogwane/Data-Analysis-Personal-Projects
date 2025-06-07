USE OnlineRetailStarSchema;
GO

--Total Sales
SELECT SUM(TotalPrice) AS total_sales FROM fact_sales;

--Top 10 Products by Revenue
SELECT TOP 10 p.description, SUM(f.TotalPrice) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.stockcode = p.stockcode
GROUP BY p.description
ORDER BY revenue DESC;

--Monthly Revenue Trend
SELECT d.[Year Month], SUM(f.TotalPrice) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.invoicedate = d.date
GROUP BY d.[Year Month]
ORDER BY d.[Year Month];


-- Average Order Value (AOV)
SELECT 
  SUM(TotalPrice) / COUNT(DISTINCT invoiceno) AS avg_order_value
FROM fact_sales;

--Customer Lifetime Value (CLV)
SELECT TOP 10
    c.customerid,
    SUM(f.TotalPrice) AS customer_lifetime_value
FROM fact_sales f
JOIN dim_customer c ON f.customerid = c.customerid
GROUP BY c.customerid
ORDER BY customer_lifetime_value DESC;


--Repeat vs One-time Customers
WITH CustomerOrders AS (
    SELECT
        customerid,
        COUNT(DISTINCT invoiceno) AS orders
    FROM fact_sales
    GROUP BY customerid
),
CustomerType AS (
    SELECT
        customerid,
        orders,
        CASE
            WHEN orders > 1 THEN 'Repeat Customer'
            ELSE 'One-time Customer'
        END AS customer_type
    FROM CustomerOrders
)
SELECT
    customer_type,
    COUNT(customerid) AS count_customers
FROM CustomerType
GROUP BY customer_type;


--Rolling 3-Month Revenue
SELECT 
  d.date,
  SUM(f.TotalPrice) OVER (
    ORDER BY d.date
    ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
  ) AS rolling_3_month_revenue
FROM fact_sales f
JOIN dim_date d ON f.invoicedate = d.date;

--RFM Segmentation
WITH rfm AS (
  SELECT 
    f.customerid,
    MAX(f.invoicedate) AS last_purchase_date,
    COUNT(DISTINCT f.invoiceno) AS frequency,
    SUM(f.TotalPrice) AS monetary
  FROM fact_sales f
  GROUP BY f.customerid
),
now_date AS (
  SELECT MAX(invoicedate) AS today FROM fact_sales
)
SELECT 
  r.customerid,
  DATEDIFF(day, r.last_purchase_date, n.today) AS recency,
  r.frequency,
  r.monetary
FROM rfm r, now_date n;



-- Inactive Customers (Churn Candidates) > 6 months relative to the latest sales date in the dataset
SELECT
    f.customerid
FROM
    fact_sales f
GROUP BY
    f.customerid
HAVING
    MAX(f.InvoiceDate) < DATEADD(month, -6, (SELECT MAX(InvoiceDate) FROM fact_sales));