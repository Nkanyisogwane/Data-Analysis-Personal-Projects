import pandas as pd
import numpy as np # Often useful for NaN handling later

# Define the path to your Excel file
# Make sure 'OnlineRetail.xlsx' is in the same directory as this script,
# or provide the full path to the file.
file_path = 'OnlineRetail.xlsx'

# Load the Excel file into a pandas DataFrame
# The header parameter assumes the first row contains column names.
try:
    df = pd.read_excel(file_path, header=0)
    print(f"Successfully loaded '{file_path}'. Shape: {df.shape}")
    print("\nFirst 5 rows of the DataFrame:")
    print(df.head())
    print("\nDataFrame Info (data types, non-null counts):")
    df.info()

    # --- Initial Data Cleaning (Crucial for this dataset) ---
    # This dataset often has missing CustomerIDs and negative quantities/prices.
    # We will perform some basic cleaning to ensure the analyses are meaningful.

    # Remove rows with missing CustomerID (as RFM requires CustomerID)
    original_rows = len(df)
    df.dropna(subset=['CustomerID'], inplace=True)
    print(f"\nRemoved {original_rows - len(df)} rows with missing CustomerID.")

    # Convert CustomerID to integer (after dropping NaNs)
    df['CustomerID'] = df['CustomerID'].astype(int)

    # Remove rows where Quantity is less than or equal to 0 (returns, cancelled orders)
    original_quantity_rows = len(df)
    df = df[df['Quantity'] > 0]
    print(f"Removed {original_quantity_rows - len(df)} rows with Quantity <= 0.")

    # Remove rows where UnitPrice is less than or equal to 0 (free items, errors)
    original_price_rows = len(df)
    df = df[df['UnitPrice'] > 0]
    print(f"Removed {original_price_rows - len(df)} rows with UnitPrice <= 0.")

    # Convert InvoiceDate to datetime objects
    # errors='coerce' will turn unparseable dates into NaT (Not a Time)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    # Drop rows where InvoiceDate could not be parsed
    original_date_rows = len(df)
    df.dropna(subset=['InvoiceDate'], inplace=True)
    print(f"Removed {original_date_rows - len(df)} rows with invalid InvoiceDate.")

    # Create TotalPrice column
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    print("\n'TotalPrice' column created.")

    print(f"\nCleaned DataFrame shape: {df.shape}")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

