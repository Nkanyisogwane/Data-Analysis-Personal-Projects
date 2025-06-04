-- Check the first few rows
SELECT TOP 10 * 
FROM dbo.Fraud;

--Count the total number of transactions
SELECT COUNT(*) AS TotalTransactions 
FROM dbo.Fraud;

--Identify invalid numerical values
SELECT * 
FROM dbo.Fraud
WHERE ISNUMERIC(amount) = 0
   OR ISNUMERIC(oldbalanceOrg) = 0
   OR ISNUMERIC(newbalanceOrig) = 0
   OR ISNUMERIC(oldbalanceDest) = 0
   OR ISNUMERIC(newbalanceDest) = 0;

--Convert amount to a numeric type
ALTER TABLE dbo.Fraud
ALTER COLUMN amount FLOAT;


--Total amount of transactions
SELECT SUM(amount) AS TotalTransactionAmount 
FROM dbo.Fraud;


--Average transaction amount by type
SELECT type, AVG(amount) AS AvgTransactionAmount 
FROM dbo.Fraud
GROUP BY type
ORDER BY AvgTransactionAmount DESC;

--Count the number of fraudulent transactions
SELECT COUNT(*) AS FraudulentTransactions 
FROM dbo.Fraud
WHERE isFraud = '1';

--Total amount involved in fraud
SELECT SUM(amount) AS TotalFraudAmount 
FROM dbo.Fraud
WHERE isFraud = '1';

--Fraudulent transactions by type
SELECT type, COUNT(*) AS FraudulentCount, SUM(amount) AS FraudulentAmount 
FROM dbo.Fraud
WHERE isFraud = '1'
GROUP BY type
ORDER BY FraudulentAmount DESC;


-- Retrieve the top 10 accounts with the highest total outgoing transaction amount
SELECT TOP 10 nameOrig, SUM(CAST(amount AS DECIMAL(18, 2))) AS TotalOutgoing
FROM dbo.Fraud
GROUP BY nameOrig
ORDER BY TotalOutgoing DESC;

--Accounts with mismatched balances (potential anomalies)
SELECT 
    nameOrig, 
    oldbalanceOrg, 
    newbalanceOrig, 
    amount
FROM 
    dbo.Fraud
WHERE 
    ABS(
        TRY_CAST(oldbalanceOrg AS DECIMAL(18, 2)) - 
        TRY_CAST(newbalanceOrig AS DECIMAL(18, 2)) - 
        TRY_CAST(amount AS DECIMAL(18, 2))
    ) > 0.01;


--Transactions flagged as fraud
SELECT COUNT(*) AS FlaggedFraudTransactions 
FROM dbo.Fraud
WHERE isFlaggedFraud = '1';

--Analyze flagged fraud transactions by type
SELECT type, COUNT(*) AS FlaggedCount, SUM(amount) AS FlaggedAmount 
FROM dbo.Fraud
WHERE isFlaggedFraud = '1'
GROUP BY type
ORDER BY FlaggedAmount DESC;


--Correlation between flagged and actual fraud
SELECT 
    SUM(CASE WHEN isFraud = '1' AND isFlaggedFraud = '1' THEN 1 ELSE 0 END) AS CorrectlyFlaggedFraud,
    SUM(CASE WHEN isFraud = '1' AND isFlaggedFraud = '0' THEN 1 ELSE 0 END) AS MissedFraud,
    SUM(CASE WHEN isFraud = '0' AND isFlaggedFraud = '1' THEN 1 ELSE 0 END) AS FalseFlags
FROM dbo.Fraud;


--Top 5 suspicious accounts (highest fraud count)
SELECT TOP 5 
    nameOrig, 
    COUNT(*) AS FraudCount, 
    SUM(TRY_CAST(amount AS DECIMAL(18, 2))) AS FraudAmount
FROM 
    dbo.Fraud
WHERE 
    isFraud = '1'
GROUP BY 
    nameOrig
ORDER BY 
    FraudCount DESC;


-- Fraud-to-Non-Fraud ratio
SELECT 
    SUM(CASE WHEN isFraud = '1' THEN 1 ELSE 0 END) AS FraudulentTransactions,
    SUM(CASE WHEN isFraud = '0' THEN 1 ELSE 0 END) AS NonFraudulentTransactions,
    CAST(SUM(CASE WHEN isFraud = '1' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS FraudRatio
FROM dbo.Fraud;


--Fraud distribution by transaction step (time)
SELECT step, COUNT(*) AS FraudCount 
FROM dbo.Fraud
WHERE isFraud = '1'
GROUP BY step
ORDER BY step;


