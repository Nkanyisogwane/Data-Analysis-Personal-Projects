
--check column names and data types
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'BankData';

--View Sample Data
SELECT TOP 10 * FROM dbo.BankData;

--Count Total Records
SELECT COUNT(*) AS Total_Records FROM dbo.BankData;

-- Check for Missing or Null Values
SELECT 
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS Age_Null,
    SUM(CASE WHEN job IS NULL THEN 1 ELSE 0 END) AS Job_Null,
    SUM(CASE WHEN balance IS NULL THEN 1 ELSE 0 END) AS Balance_Null
FROM dbo.BankData;
	

--Total Customers by Job (All Customers)
SELECT job, COUNT(*) AS Total_Customers 
FROM dbo.BankData
GROUP BY job
ORDER BY Total_Customers DESC;

--Deposits by Job Type
SELECT job, 
       COUNT(*) AS Total_Customers, 
       SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS Deposits_Made
FROM dbo.BankData
GROUP BY job
ORDER BY Deposits_Made DESC;

--Average Balance by Marital Status
SELECT marital, AVG(CAST(balance AS FLOAT)) AS Avg_Balance
FROM dbo.BankData
GROUP BY marital;

-- Deposit Conversion Rate Calculation
SELECT 
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS Deposits_Made,
    (SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS Deposit_Conversion_Rate
FROM dbo.BankData;

-- Deposits by Job Type (Top Performers)
SELECT 
    job,
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS Deposits_Made,
    (SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS Deposit_Conversion_Rate
FROM dbo.BankData
GROUP BY job
ORDER BY Deposit_Conversion_Rate DESC;

--Impact of Balance on Deposits
SELECT 
    deposit,
    AVG(CAST(balance AS FLOAT)) AS Avg_Balance
FROM dbo.BankData
GROUP BY deposit;


--Monthly Deposit Trends
SELECT 
    month, 
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS Deposits_Made,
    (SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS Deposit_Conversion_Rate
FROM dbo.BankData
GROUP BY month
ORDER BY 
    CASE month
        WHEN 'jan' THEN 1
        WHEN 'feb' THEN 2
        WHEN 'mar' THEN 3
        WHEN 'apr' THEN 4
        WHEN 'may' THEN 5
        WHEN 'jun' THEN 6
        WHEN 'jul' THEN 7
        WHEN 'aug' THEN 8
        WHEN 'sep' THEN 9
        WHEN 'oct' THEN 10
        WHEN 'nov' THEN 11
        WHEN 'dec' THEN 12
        ELSE 13 -- For any unexpected values
    END;


--Effect of Previous Campaigns on Deposits
SELECT 
    poutcome,
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS Deposits_Made,
    (SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS Deposit_Conversion_Rate
FROM dbo.BankData
GROUP BY poutcome
ORDER BY Deposit_Conversion_Rate DESC;


