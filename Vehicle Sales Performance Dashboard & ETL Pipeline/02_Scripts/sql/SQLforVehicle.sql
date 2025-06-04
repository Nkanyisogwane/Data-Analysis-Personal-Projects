-- Monthly Sales Trend
SELECT 
    CONVERT(VARCHAR(7), saledate, 120) AS sale_month,
    COUNT(*) AS total_vehicles_sold,
    SUM(CAST(sellingprice AS DECIMAL(18,2))) AS total_revenue,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2))), 2) AS avg_price
FROM clean_vehicle_sales
WHERE saledate IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
GROUP BY CONVERT(VARCHAR(7), saledate, 120)
ORDER BY sale_month;


--Top 10 Brands by Revenue and Volume
SELECT TOP 10
    make,
    COUNT(*) AS total_sold,
    ROUND(SUM(CAST(sellingprice AS DECIMAL(18,2))), 0) AS total_sales,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2))), 0) AS avg_price
FROM clean_vehicle_sales
WHERE make IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
GROUP BY make
ORDER BY total_sales DESC;


--Average Price Gap by Brand
SELECT 
    make,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2)) - CAST(mmr AS DECIMAL(18,2))), 2) AS avg_price_diff,
    ROUND(AVG(
        CASE 
            WHEN CAST(mmr AS DECIMAL(18,2)) = 0 THEN NULL
            ELSE (CAST(sellingprice AS DECIMAL(18,2)) - CAST(mmr AS DECIMAL(18,2))) / 
                 CAST(mmr AS DECIMAL(18,2))
        END
    ), 2) AS avg_margin_pct
FROM clean_vehicle_sales
WHERE mmr IS NOT NULL 
    AND sellingprice IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
    AND TRY_CAST(mmr AS DECIMAL(18,2)) IS NOT NULL
GROUP BY make
ORDER BY avg_price_diff DESC;


--Condition Based Pricing
SELECT 
    condition,
    COUNT(*) AS vehicle_count,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2))), 0) AS avg_selling_price,
    ROUND(AVG(CAST(mmr AS DECIMAL(18,2))), 0) AS avg_mmr,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2)) - CAST(mmr AS DECIMAL(18,2))), 0) AS avg_price_difference
FROM clean_vehicle_sales
WHERE condition IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
    AND TRY_CAST(mmr AS DECIMAL(18,2)) IS NOT NULL
GROUP BY condition
ORDER BY avg_selling_price DESC;


--State level revenue breakdown
SELECT 
    state,
    COUNT(*) AS vehicles_sold,
    SUM(CAST(sellingprice AS DECIMAL(18,2))) AS total_revenue,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2))), 0) AS avg_price,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2)) - CAST(mmr AS DECIMAL(18,2))), 0) AS avg_price_vs_mmr
FROM clean_vehicle_sales
WHERE state IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
    AND TRY_CAST(mmr AS DECIMAL(18,2)) IS NOT NULL
GROUP BY state
ORDER BY total_revenue DESC;


--Transmission Type Trends
SELECT 
    transmission,
    COUNT(*) AS total_sold,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2))), 0) AS avg_price,
    ROUND(AVG(CAST(sellingprice AS DECIMAL(18,2)) - CAST(mmr AS DECIMAL(18,2))), 0) AS avg_price_vs_market,
    COUNT(DISTINCT model) AS unique_models_available
FROM clean_vehicle_sales
WHERE transmission IS NOT NULL
    AND TRY_CAST(sellingprice AS DECIMAL(18,2)) IS NOT NULL
    AND TRY_CAST(mmr AS DECIMAL(18,2)) IS NOT NULL
GROUP BY transmission
ORDER BY total_sold DESC;