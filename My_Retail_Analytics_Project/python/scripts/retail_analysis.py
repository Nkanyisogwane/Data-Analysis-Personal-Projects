import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import warnings
import os
from datetime import datetime

# =============================================
# 1. INITIAL SETUP & CONFIGURATION
# =============================================
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

# =============================================
# 2. DATA LOADING & CLEANING
# =============================================
def load_and_clean_data(file_path):
    """Load and clean the retail data"""
    try:
        print(f"\n{'='*50}\nLoading data from: {file_path}\n{'='*50}")
        df = pd.read_excel(file_path, header=0)
        print(f"Initial shape: {df.shape}")
        
        # Convert InvoiceDate to datetime objects, specifically handling Excel's serial date format
        if pd.api.types.is_numeric_dtype(df['InvoiceDate']):
            # If InvoiceDate is numerical (Excel serial date number), convert it
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], unit='D', origin='1899-12-30')
            print("Converted InvoiceDate from Excel serial number.")
        else:
            # If InvoiceDate is read as a string or actual datetime object (which it often is directly from read_excel)
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
            print("Converted InvoiceDate from string/datetime.")

        date_nan_count = df['InvoiceDate'].isna().sum()
        df.dropna(subset=['InvoiceDate'], inplace=True)
        if date_nan_count > 0:
            print(f"Removed {date_nan_count} rows with invalid InvoiceDate.")
        else:
            print("No invalid InvoiceDate rows found after conversion.")
        
        # Clean CustomerID
        original_cust_rows = len(df)
        df = df[df['CustomerID'].notna()]
        df['CustomerID'] = df['CustomerID'].astype(int) # After dropping NaNs, convert to int
        print(f"Removed {original_cust_rows - len(df)} rows with missing CustomerID.")
        
        # Clean quantities and prices
        original_qty_price_rows = len(df)
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
        print(f"Removed {original_qty_price_rows - len(df)} rows with Quantity <= 0 or UnitPrice <= 0.")
        
        # Create derived columns
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period('M')
        
        print(f"\nCleaned shape: {df.shape}")
        print("\nSample data after cleaning and date fix:")
        print(df.head(3))
        return df
    
    except Exception as e:
        print(f"\nERROR during data loading/cleaning: {str(e)}")
        return None

# =============================================
# 3. SALES ANALYSIS
# =============================================
def analyze_sales(df):
    """Perform sales trend analysis"""
    print(f"\n{'='*50}\nSales Analysis\n{'='*50}")
    
    # Daily sales trend
    daily_sales = df.set_index('InvoiceDate')['TotalPrice'].resample('D').sum()
    
    plt.figure(figsize=(15, 7))
    daily_sales.plot(title='Daily Sales Trend', label='Daily Sales', alpha=0.8)
    daily_sales.rolling(window=30).mean().plot(label='30-Day Moving Avg', color='red', linewidth=2)
    plt.legend()
    plt.ylabel('Total Sales')
    plt.xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Monthly sales
    monthly_sales = df.groupby('InvoiceYearMonth')['TotalPrice'].sum()
    print("\nMonthly Sales:")
    print(monthly_sales)

# =============================================
# 4. RFM ANALYSIS & CUSTOMER SEGMENTATION
# =============================================
def perform_rfm_analysis(df):
    """Perform RFM analysis and customer segmentation"""
    print(f"\n{'='*50}\nRFM Customer Segmentation\n{'='*50}")
    
    # Define a snapshot date for Recency calculation - typically one day after the last invoice date in the dataset
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('CustomerID').agg(
        Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days), # Days since last purchase
        Frequency=('InvoiceNo', 'nunique'), # Number of unique orders
        Monetary=('TotalPrice', 'sum') # Total money spent
    ).reset_index()
    
    # Drop rows where Monetary is 0 or NaN, as these customers won't be useful for RFM analysis
    rfm.dropna(subset=['Monetary'], inplace=True)
    rfm = rfm[rfm['Monetary'] > 0]

    if len(rfm) > 0: # Ensure there's data for KMeans
        # KMeans clustering
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
            rfm['Segment'] = kmeans.fit_predict(rfm[['Recency', 'Frequency', 'Monetary']])
        
        # Segment analysis
        segment_stats = rfm.groupby('Segment').agg(
            AvgRecency=('Recency', 'mean'),
            AvgFrequency=('Frequency', 'mean'),
            AvgMonetary=('Monetary', 'mean'),
            NumCustomers=('CustomerID', 'count')
        ).sort_values(by='AvgMonetary', ascending=False) # Sort by Monetary for easy interpretation
        
        print("\nCustomer Segments:")
        print(segment_stats)
        
        # Visualize segments
        plt.figure(figsize=(12, 8))
        sns.scatterplot(data=rfm, x='Frequency', y='Monetary', hue='Segment', palette='viridis', s=80, alpha=0.7)
        plt.title('Customer Segments by Frequency vs Monetary Value')
        plt.xlabel('Frequency (Number of Orders)')
        plt.ylabel('Monetary Value (Total Spent)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return rfm # Return the rfm DataFrame
    else:
        print("No valid customer data for RFM segmentation after cleaning.")
        return None # Return None if no valid data

# =============================================
# 5. PRODUCT ANALYSIS
# =============================================
def analyze_products(df):
    """Analyze product performance"""
    print(f"\n{'='*50}\nProduct Analysis\n{'='*50}")
    
    # Top products
    top_products = df.groupby('Description')['TotalPrice'].sum().nlargest(10)
    
    if not top_products.empty:
        plt.figure(figsize=(12, 6))
        top_products.sort_values().plot(kind='barh', color='skyblue')
        plt.title('Top 10 Products by Revenue')
        plt.xlabel('Total Revenue')
        plt.ylabel('Product Description')
        plt.tight_layout()
        plt.show()
    else:
        print("No product sales data to plot.")
    
    # StockCode analysis
    if 'StockCode' in df.columns:
        print("\nTop 5 Stock Codes by Frequency:")
        print(df['StockCode'].value_counts().head())

# =============================================
# MAIN EXECUTION
# =============================================
if __name__ == "__main__":
    # Configuration
    file_path = 'OnlineRetail.xlsx'
    
    # Check file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        exit()
    
    # Run all analyses
    start_time = datetime.now()
    print(f"\nAnalysis started at: {start_time}")
    
    retail_data = load_and_clean_data(file_path)
    
    if retail_data is not None and not retail_data.empty:
        # Perform RFM analysis and capture the returned rfm DataFrame
        rfm_segments_df = perform_rfm_analysis(retail_data)
        analyze_sales(retail_data) # Call sales analysis after RFM as it uses retail_data
        analyze_products(retail_data) # Call product analysis

        # --- Export RFM Segments to CSV ---
        # Make sure rfm_segments_df DataFrame exists and has 'CustomerID' and 'Segment'
        if rfm_segments_df is not None and 'CustomerID' in rfm_segments_df.columns and 'Segment' in rfm_segments_df.columns:
            output_rfm_path = 'customer_segments.csv'
            rfm_segments_df[['CustomerID', 'Segment']].to_csv(output_rfm_path, index=False)
            print(f"\nExported customer segments to '{output_rfm_path}'")
        else:
            print("\nRFM DataFrame or required columns not found for export.")

    else:
        print("Data is empty or not loaded correctly. Cannot proceed with analysis.")
    
    end_time = datetime.now()
    print(f"\nAnalysis completed at: {end_time}")
    print(f"Total runtime: {end_time - start_time}")

