import pandas as pd
import re

# ----------------------------------------------------
# STEP 1: Load the dataset
# ----------------------------------------------------
# Replace 'your_file_name.csv' with the actual name of your CSV file.
try:
    df = pd.read_csv('Warehouse_and_Retail_Sales.csv')
except FileNotFoundError:
    print("Error: The file was not found. Please make sure the CSV file is in the same directory as this script.")
    exit()

# ----------------------------------------------------
# STEP 2: Clean the numeric columns
# ----------------------------------------------------
# The goal is to remove any non-numeric characters (like currency symbols or spaces)
# and convert the columns to a numeric format.

# List of columns that should be numeric
numeric_columns = [
    'RETAIL SALES',
    'RETAIL TRANSFERS',
    'WAREHOUSE SALES'
]

for col in numeric_columns:
    # Use a regular expression to remove everything except numbers and a decimal point.
    # The [^0-9\.] part matches any character that is NOT a digit or a decimal point.
    # We replace these characters with an empty string.
    df[col] = df[col].astype(str).str.replace(r'[^0-9\.]', '', regex=True)
    
    # After cleaning, convert the column to a numeric data type.
    # pd.to_numeric() is robust and will handle the conversion.
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ----------------------------------------------------
# STEP 3: Convert other columns to their correct types
# ----------------------------------------------------
# YEAR and MONTH are already integers, but it's good practice to ensure they are.
df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').astype('Int64')
df['MONTH'] = pd.to_numeric(df['MONTH'], errors='coerce').astype('Int64')

# Item Code is an identifier, so it can be an integer.
df['ITEM CODE'] = pd.to_numeric(df['ITEM CODE'], errors='coerce').astype('Int64')

# Supplier, Item Description, and Item Type are text/categorical.
# The 'string' type in pandas is more memory-efficient than 'object'
df['SUPPLIER'] = df['SUPPLIER'].astype('string')
df['ITEM DESCRIPTION'] = df['ITEM DESCRIPTION'].astype('string')
df['ITEM TYPE'] = df['ITEM TYPE'].astype('string')

# ----------------------------------------------------
# STEP 4: Save the cleaned DataFrame to a new CSV file
# ----------------------------------------------------
cleaned_file_name = 'cleaned_sales_data.csv'
df.to_csv(cleaned_file_name, index=False)

print(f"Data cleaning complete! The cleaned data has been saved to: {cleaned_file_name}")

# Display the first few rows of the cleaned data for confirmation
print("\nFirst 5 rows of the cleaned data:")
print(df.head())
