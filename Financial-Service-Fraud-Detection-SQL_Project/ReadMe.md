# Financial Service Fraud Detection: SQL Project  

## 📖 Overview  
This project is a deep dive into SQL, focusing on exploring, analyzing, and drawing insights from a financial services fraud detection dataset. It is part of my journey to strengthen my SQL skills and prepare for a career as a Data Analyst.  

The dataset, named `Fraud.csv`, contains records of transactions labeled as fraudulent or legitimate. I analyzed this data using SQL Server, performing tasks such as data validation, aggregation, anomaly detection, and fraud analysis.  

---

## 🚀 Purpose  
After stepping away from SQL for some time, I wanted a project to help me:  
- Rebuild my confidence in SQL.  
- Learn new techniques and approaches to SQL analysis.  
- Prepare for real-world data analysis scenarios.  

This project combines learning and problem-solving while creating something valuable to showcase to recruiters.

---

## 🛠 Methodology  
For this project, I loaded the dataset into SQL Server, performed data cleaning, and ran multiple queries to extract insights. Below, you’ll find **a few key queries with explanations and screenshots** of their results.  

Additionally, **all queries used in the project are included in the SQL file** (`AllQueries.sql`) in this repository.  

---

### **Queries and Results**  

#### **1. View Sample Data**  
```sql
-- Check the first few rows
SELECT TOP 10 * 
FROM dbo.Fraud;

---

This query allowed me to get a sense of the data structure and content.


-- Count the total number of transactions
SELECT COUNT(*) AS TotalTransactions 
FROM dbo.Fraud;
This query was essential to understand the dataset size and the scale of analysis required.

-- Count the number of fraudulent transactions
SELECT COUNT(*) AS FraudulentTransactions 
FROM dbo.Fraud
WHERE isFraud = '1';
I was surprised by how small the proportion of fraudulent transactions was. This query provided a good starting point for further analysis.

-- Retrieve the top 10 accounts with the highest total outgoing transaction amount
SELECT TOP 10 nameOrig, SUM(CAST(amount AS DECIMAL(18, 2))) AS TotalOutgoing
FROM dbo.Fraud
GROUP BY nameOrig
ORDER BY TotalOutgoing DESC;
This query showed which accounts were responsible for the largest outgoing transactions, helping to identify potentially suspicious activity.

-- Accounts with mismatched balances (potential anomalies)
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

This query highlighted discrepancies in account balances, suggesting potential errors or fraudulent behavior.


🌟 Key Insights
Most fraudulent transactions were of the type TRANSFER.
Some accounts had anomalies in their balances, indicating potential suspicious activity.
Fraudulent transactions were concentrated in specific time steps, which could help in fraud prevention strategies.

🤖 How I Used AI
To be transparent, I relied on ChatGPT to help streamline my learning process and queries. Here's how AI contributed:

Learning: Instead of spending hours searching for solutions across multiple platforms, I used ChatGPT to clarify concepts, troubleshoot errors, and guide me through best practices.
Problem-Solving: While I didn’t know all the queries upfront, ChatGPT helped me think through problems logically and write optimized SQL code.
Reflection: AI was a tool, but the critical thinking, debugging, and understanding were entirely mine. This project proved that I am an adaptable and resourceful problem-solver.

📚 Lessons Learned
SQL is a powerful tool for fraud detection, and even small queries can uncover big insights.
Using AI tools like ChatGPT can accelerate the learning process while still requiring critical thinking and effort.
This project has reignited my passion for data analysis and reminded me of my ability to tackle complex problems.

🗂 Repository Contents
README.md – This file contains a project overview and key queries with explanations.
Screenshots/ – A folder containing screenshots of query results (referenced above).
AllQueries.sql – A file containing all the SQL queries used in this project.

🔗 Conclusion
This project showcases my ability to use SQL to extract insights, solve problems, and document findings in a professional manner. While I relied on AI to enhance my learning, I combined this guidance with critical thinking to complete the project independently.

Check out the full project, including queries and results, in the repository.


