# 🛒 Online Retail Sales Performance Analytics

## 📌 Project Overview
This project focuses on performing an end-to-end sales performance analysis for an online retail company. Leveraging a comprehensive dataset, the goal was to:
- Transform raw transactional data into actionable insights  
- Identify key sales trends  
- Understand customer behavior through segmentation  
- Visualize performance in an interactive Power BI dashboard

## 🎯 Business Problem & Goal
The online retail company needed a robust solution to understand its sales dynamics, identify top-performing products and customers, analyze geographical sales distribution, and segment customers for targeted marketing efforts.

**Key challenges included:**
- Dealing with raw, messy transactional data  
- Normalizing the data model for better analytics  
- Extracting customer behavior patterns  
- Creating a dashboard that supports business decisions

## 📂 Dataset Description

**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/)

**Name:** Online Retail Dataset  
**Rows:** 396,670  

**Key Columns:**
- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

---

## 🛠 Tools & Technologies

- **Power BI**: For data modeling, dashboard creation, and interactive visualizations  
- **Power Query**: For data cleaning and transformation within Power BI  
- **DAX**: For calculated columns, measures, and Key Performance Indicators (KPIs)  
- **Python** *(Pandas, scikit-learn, Matplotlib, Seaborn)*: For extensive data cleaning, advanced statistical analysis (RFM segmentation, K-Means clustering), and analytical plotting  
- **SQL Server**: Used as the relational database for storing cleaned and structured data  
- **SQL**: For generating analytical queries and extracting specific insights from the database  
- **Excel**: The initial raw data source, also used for intermediate steps during data handling challenges  
- **DAX Studio**: Utilized for extracting data from Power BI model for SQL Server import attempts  
- **ODBC Driver 17 for SQL Server**: Essential for connecting Python to SQL Server

## 📊 Quick Stats

Here’s a snapshot of the key performance indicators derived from the analysis:

| Metric | Value |
|--------|-------|
| 🛍️ Total Sales | R8.76M |
| 🧾 Total Invoices | 18K |
| 👥 Unique Customers | 4,335 |
| 🏆 Top Product | PAPER CRAFT, LITTLE BIRDIE (R168K in sales) |
| 📉 At-Risk Customers | 4,296 (Segment 0)<br>Avg. Recency: 93.8 days<br>Avg. Monetary: R1.4K |
| 📈 Peak Sales Month (UK) | November (11.87% of UK Total Sales) |

---

## 🧱 Data Modeling Approach

A **Star Schema** approach was applied in Power BI, splitting the original transactional data into **Fact** and **Dimension** tables to enhance performance and support flexible analytics.

### 🧾 Fact Table: `FactSales`
Contains raw transaction-level data with relevant foreign keys:
- `InvoiceNo`, `StockCode`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`

**Calculated Column:**
- `TotalPrice` = `Quantity` × `UnitPrice`

### 🧍 Dimension Tables:
- **DimCustomer**: `CustomerID` (unique customer identifiers)
- **DimProduct**: `StockCode`, `Description` (product details)
- **DimCountry**: `Country` (geographical data)
- **DimDate**: DAX-generated date table with hierarchy (Year, Month, Quarter, Day)

## ⚙️ Project Architecture & Methodology

The project followed a structured, iterative approach to address real-world data challenges through each stage of the pipeline.

### 1️⃣ Data Acquisition & Initial Transformation (Python)

- **Source**: Raw transactional data in `.xlsx` format (downloaded from Kaggle)
- **Initial Issues Identified**:
  - Missing `CustomerID` values
  - Negative `Quantity` and `UnitPrice` values (indicating returns or errors)
  - Inconsistent `StockCode` formats (e.g., 'POST', alphanumeric noise)
  - Excel serial-based `InvoiceDate` requiring parsing

#### ⚠️ Challenge: Power BI Excel Ingestion Errors

Power BI failed to connect directly to the Excel file via OLEDB due to:
- 32-bit/64-bit driver conflicts
- General connection instability

#### ✅ Solution: Python Script for Data Preprocessing

A Python script was developed to:
- Filter out rows with:
  - Missing `CustomerID`
  - Negative `Quantity` or non-positive `UnitPrice`
- Standardize `StockCode` by:
  - Removing non-product entries (e.g., 'POST')
  - Ensuring consistent formatting
- Parse `InvoiceDate` from Excel serial to proper `datetime` format
- Fix data types (e.g., `CustomerID` as `int`, `UnitPrice` and `Quantity` as `float/int`)

**➡️ Output**: Cleaned and normalized `.csv` files for star schema modeling:
- `dim_country.csv`
- `dim_customer.csv`
- `dim_date.csv`
- `dim_product.csv`
- `fact_sales.csv`

### 2️⃣ Data Modeling (Power BI Star Schema)

Imported the cleaned `.csv` files into Power BI Desktop to build an analytical data model.

#### ⚠️ Challenge: Duplicates & Referential Integrity

Initial modeling issues included:
- Ensuring **unique keys** in dimension tables (e.g., `DimCustomer`, `DimProduct`)
- Maintaining **referential integrity** between fact and dimension tables

#### ✅ Solution: Power Query Cleanup

- Applied granular transformations in **Power Query**:
  - Removed duplicate rows in dimension tables
  - Verified consistency of foreign keys across tables

- Established **one-to-many relationships** from:
  - `FactSales` ➡️ `DimProduct`
  - `FactSales` ➡️ `DimCustomer`
  - `FactSales` ➡️ `DimDate`
  - `FactSales` ➡️ `DimCountry`

**🧱 Result**: A clean, performant **Star Schema model** enabling accurate analytics.

📸 *Data Model Screenshot Placeholder*

---

### 3️⃣ Key Performance Indicator (KPI) Calculation

Developed core business KPIs using DAX in Power BI:

- **Total Sales**  
- **Total Quantity Sold**  
- **Total Invoices**  
- **Average Order Value**  
- **Unique Customers**

These KPIs served as foundational insights for the dashboard.

### 4️⃣ Exploratory Data Analysis & Advanced Analytics (Python)

Performed comprehensive data exploration and statistical analysis using Python.

#### 📈 Sales Trend Analysis
- Utilized `.describe()` for statistical summary
- Analyzed **daily and monthly sales trends**
- Incorporated **30-day rolling averages** to smooth volatility

🖼️ *Python Plot: Daily Sales Trend*

**🔍 Insight**: 
Despite fluctuations, sales showed an **upward trend** toward year-end, indicating **seasonal patterns** — particularly relevant for inventory planning and campaign timing.

---

#### 👥 Customer Segmentation (RFM Analysis)

Executed **Recency, Frequency, and Monetary (RFM)** analysis:
- Used `scikit-learn`’s **K-Means clustering**
- Segmented customers into 4 groups:
  - *Champions*
  - *Loyal*
  - *At-Risk*
  - *Lapsed*

🖼️ *Python Plot: Customer Segments by Frequency vs. Monetary Value*

**🔍 Insight**:
Clear segmentation showed small but high-value customers were well-separated from the lower-value, infrequent purchasers — critical for targeted marketing.

---

#### 🏆 Product Performance Analysis

- Identified **Top 10 products** by total revenue
- Analyzed **StockCode frequency** to detect product popularity

🖼️ *Python Plot: Top 10 Products by Revenue*

**🔍 Insight**:
A small group of products (e.g., *PAPER CRAFT , LITTLE BIRDIE*) accounted for a **disproportionate share of revenue** — a signal for strategic stock and promotional focus.

---

#### 🔄 Power BI Integration

Exported `CustomerID` with assigned RFM segment to `customer_segments.csv` for seamless use in Power BI dashboard filters and visualizations.

## 5️⃣ SQL Server Integration & Analytical Queries

### ⚠️ Challenge: SQL Server Import Roadblocks & Driver Compatibility  
Initial efforts to export Power BI-prepared tables (via DAX Studio to Excel) and import into SQL Server were blocked by frustrating **64-bit driver compatibility issues**.

### 💡 Solution: Python as Data Integration Layer  
- Enhanced the Python script to connect directly to SQL Server using **pyodbc** and **SQLAlchemy**.  
- Programmatically loaded cleaned dimension and fact tables (.csv files) into SQL Server with `to_sql()` method.  
- Ensured **seamless and reliable database population** process, bypassing previous driver issues.

---

### 🔍 SQL Query Development  
Executed analytical queries directly on SQL Server to extract key business insights:

- **Customer Type Analysis:**  
  Classified customers as **'Repeat'** or **'One-time'** based on count of distinct invoices — showcasing aggregation and customer behavior categorization.

- **Inactive Customer Identification (Churn Candidates):**  
  Identified customers with **no purchases for over 6 months** relative to the latest sales date, enabling early **churn prediction** and retention strategies.

## 6️⃣ Interactive Dashboard Development (Power BI)

### 🎨 Dashboard Design  
- Created a **visually appealing and intuitive Power BI dashboard** showcasing Global Sales Performance.  
- Included key visuals: overall KPIs, sales trends, top products, and top customers.

---

### 🛠 Visual Troubleshooting & Refinement  
- Fixed a **Top 5 Customers by Total Sales** bar chart issue where gaps appeared and CustomerID was treated as a continuous numeric axis, causing confusing visuals.  
- Solution: Changed **CustomerID data type to Text** in Power BI data model.  
- Adjusted Y-axis formatting to **disable "Show items with no data"**, ensuring only relevant customers displayed.

---

### ⚡ Enhanced Interactivity  
- Added essential slicers for dynamic dashboard filtering:  
  - **Month/Year Slicer** for time-based analysis  
  - **Country Slicer** for geographic insights  
  - **Customer Segment Slicer** integrating Python-derived RFM clusters, enabling targeted insights by segment  
- Carefully modeled relationships between **customer_segments.csv** and **DimCustomer** table to support filtering.  
- Implemented a **"Reset Slicers" button** via Power BI Bookmarks for improved user experience.

---

### 📸 Final Dashboard Screenshot  
*(Insert screenshot here)*

## 📈 Key Insights & Analysis Performed

The comprehensive analysis yielded several actionable insights:

### 🧮 Overall Performance
- The company generated **R8.76 Million** in Total Sales from **5 Million units** and **18 Thousand invoices**, serving **4,335 unique customers**.  
- This highlights a significant scale of operations.

### 🔝 Product Performance
- The highest revenue-generating product was **"PAPER CRAFT , LITTLE BIRDIE"** with sales of **R168,469.6**.  
- This product accounted for **18.22% of Total Sales** within the top 10 products, significantly outperforming lower-selling products.  
- These findings highlight top sellers for promotion and stock optimization.

### 📅 Sales Trends
- Sales showed a clear upward trajectory throughout the year, peaking significantly in **November**.  
- For example, November in the **United Kingdom** made up **11.87% of Total Sales**, indicating strong seasonal performance during holiday periods.  
- This trend can inform inventory management and marketing campaign timing.

### 🌍 Geographic Performance
- Key contributing countries and their specific sales patterns over time were identified.  
- This allows for region-specific strategy development.

### 🧍 Customer Segmentation
- RFM analysis classified customers into distinct groups for targeted engagement:

  - **Champions (Segment 3):**  
    - Small, highly valuable group of **2 customers**  
    - Very recent purchases (Avg. Recency: 1.5 days)  
    - High frequency (Avg. Frequency: 66 orders)  
    - Exceptionally high spend (Avg. Monetary: R269K)  
    - Ideal candidates for VIP treatment and loyalty programs.

  - **At-Risk/Lapsed Customers (Segment 0):**  
    - Largest group with **4,296 customers**  
    - Lower recency (Avg. Recency: 93.8 days)  
    - Low frequency (Avg. Frequency: 3.8 orders)  
    - Low monetary value (Avg. Monetary: R1.4K)  
    - Requires re-engagement strategies or targeted campaigns to prevent churn.

### 📊 Dynamic Insights from Narratives (Examples)
- *October in United Kingdom accounted for 20.29% of Total Sales.*  
  - **VINTAGE UNION JACK MEMOBOARD** had the highest sales at **R16,592.08**, which was **198.66% higher** than the lowest-selling **DOORMAT BLACK FLOCK** (R5,555.54).

- *January in United Kingdom accounted for 84.71% of Total Sales.*  
  - **MEDIUM CERAMIC TOP STORAGE JAR** led with **R77,183.6**, which was **1,474.54% higher** than the lowest-selling **HEART OF WICKER SMALL** (R4,901.98).

## 🔬 Advanced Analysis (Planned or Completed)

- **RFM Segmentation using Python** (Completed)  
- **SQL Churn Analysis Queries** (Completed)  
- **Price Sensitivity per Country** (Planned)  
- **Return Rate by Customer Segments** (Planned)  

## ✅ Next Steps

- Host dashboard on Power BI Service (optional)  
- Upload project to GitHub with proper documentation (**Completed: this README!**)  
- Enhance visual storytelling with bookmark pages (Planned)  
- Implement a Smart Narrative visual in Power BI for automated, dynamic textual summaries  
- Explore the Key Influencers visual to identify primary drivers of specific business outcomes  
- Add Drill-through pages in Power BI for detailed transaction-level analysis  
- Investigate Advanced DAX patterns for more complex calculations  
- Implement Time Series Forecasting in Python (e.g., using the Prophet library) to predict future sales trends and demand  

## 🙌 Acknowledgments

- **UCI Machine Learning Repository** – For providing the dataset  
- **Power BI Community** – For resources and support  
- **Stack Overflow & Medium Blogs** – For Python insights and troubleshooting guidance  

## 🔗 Connect

If you like this project or have feedback, feel free to connect with me on LinkedIn!

---

## 📁 Project Structure

\`\`\`
My_Retail_Analytics_Project/
├── README.md # Main project documentation
├── .gitignore # Git ignore file for specific files/folders
├── data/
│ ├── raw/
│ │ └── OnlineRetail.xlsx # Original, unprocessed dataset
│ └── processed/
│ ├── dim_country.csv # Cleaned CSVs used for SQL import
│ ├── dim_customer.csv
│ ├── dim_date.csv
│ ├── dim_product.csv
│ ├── fact_sales.csv
│ └── customer_segments.csv # CSV output from Python RFM analysis for Power BI
│
├── sql/
│ ├── scripts/
│ │ ├── create_star_schema_tables.sql # SQL script for creating database tables (star schema)
│ │ └── analytical_queries.sql # SQL queries for specific insights (e.g., churn, customer types)
│ └── screenshots/
│ ├── sql_query_example_1.png # Screenshots of SQL queries/results
│ └── sql_query_example_2.png
│
├── python/
│ ├── scripts/
│ │ └── retail_data_analysis.py # Main Python script for data cleaning, RFM, and analysis
│ └── plots/
│ ├── daily_sales_trend.png # Saved plots generated by Python (e.g., sales trend)
│ ├── customer_segments_scatterplot.png # Saved customer segmentation scatter plot
│ └── top_products_revenue_plot.png
│
├── powerbi/
│ ├── Online_Retail_Sales_Dashboard.pbix # The Power BI Desktop file
│ └── screenshots/
│ ├── dashboard_final_view.png # Screenshot of the final Power BI dashboard
│ └── data_model_star_schema.png # Screenshot of the Power BI data model (star schema)
│
└── requirements.txt # List of Python libraries and their versions
\`\`\`
