import pandas as pd

# 1. Load the data
df = pd.read_csv("car_prices.csv")

# 2. Quick overview
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.isnull().sum())

# 3. Convert data types - FIXED DATE PARSING
df['saledate'] = pd.to_datetime(df['saledate'], 
                               format='mixed',  # Explicitly handle mixed formats
                               utc=True,       # Handle timezones consistently
                               errors='coerce') # Still coerce errors to NaT

# Verify date conversion worked
print("\nDate conversion check:")
print(df['saledate'].head())
print("Null dates:", df['saledate'].isnull().sum())

# Only proceed if we have valid dates
if df['saledate'].notnull().any():
    # 4. Drop rows with missing key data - ADD DATE TO CRITICAL FIELDS
    df.dropna(subset=['saledate', 'sellingprice', 'mmr'], inplace=True)
    
    # 5. Create new features - NOW SAFE TO USE .dt ACCESSOR
    df['price_diff'] = df['sellingprice'] - df['mmr']
    df['profit_margin'] = (df['price_diff'] / df['mmr']).round(2)
    df['sale_year'] = df['saledate'].dt.year
    df['sale_month'] = df['saledate'].dt.month_name()  # More readable than numbers
    
    
    # 7. Final check
    print("\nCleaned data sample:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    
    # 8. Export clean data
    df.to_csv("clean_vehicle_sales.csv", index=False)
else:
    print("ERROR: Could not parse any valid dates from saledate column.")
    print("Please check the date format in your CSV file.")