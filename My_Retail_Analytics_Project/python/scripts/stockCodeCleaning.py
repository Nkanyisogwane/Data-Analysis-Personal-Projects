import pandas as pd
import re
import numpy as np # Import numpy for NaN

def clean_stockcodes(input_file, output_file):
    """
    Cleans the StockCode column in an Excel file and ensures it's numeric.
    - Keeps all other columns and rows unchanged
    - Fixes alphanumeric codes (e.g., '545614G' → '545614')
    - Removes specific non-product codes (like 'POST', 'D')
    - Converts the cleaned StockCode to a numeric type, setting unconvertible values to NaN.
    - Removes rows where StockCode is NaN after conversion.
    - Saves cleaned version to new file
    """
    # Load data
    df = pd.read_excel(input_file)
    print(f"Loaded '{input_file}' with {len(df)} rows")
    initial_rows = len(df) # To track dropped rows later

    # Clean StockCode (ONLY change made to the data)
    df['StockCode'] = df['StockCode'].astype(str)

    # Step 1: Remove trailing letters from alphanumeric codes (e.g., '545614G' -> '545614')
    # Use a new temporary column or direct assignment if you're sure about overwriting
    df['StockCode_temp'] = df['StockCode'].str.replace(r'[A-Za-z]+$', '', regex=True)

    # Step 2: Remove specific non-product codes (apply to the temp cleaned column)
    non_product_codes = ['POST', 'D', 'M', 'CRUK', 'DOT', 'ADJUST',
                         'S', 'B', 'C', 'PADS', 'A', 'P', 'R', 'K', 'C2',
                         'AMAZONFEE', 'BANK CHARGES', 'DCGS'] # Added more common ones
    # Filter df based on the cleaned temp column
    df = df[~df['StockCode_temp'].isin(non_product_codes)].copy() # Use .copy() after filtering for safety

    # Step 3: Convert the cleaned StockCode column to numeric.
    # 'errors='coerce'' will turn any value that can't be converted into NaN.
    df['StockCode_numeric'] = pd.to_numeric(df['StockCode_temp'], errors='coerce')

    # Step 4: Remove rows where StockCode could not be converted to a number.
    # These are truly invalid or non-product codes that slipped through or were malformed.
    rows_before_final_drop = len(df)
    df.dropna(subset=['StockCode_numeric'], inplace=True)
    rows_after_final_drop = len(df)
    print(f"Dropped {rows_before_final_drop - rows_after_final_drop} rows due to StockCode not being convertible to numeric.")

    # Drop the temporary column and replace original StockCode with the cleaned, numeric one
    df.drop(columns=['StockCode', 'StockCode_temp'], inplace=True) # Drop original and temp
    df.rename(columns={'StockCode_numeric': 'StockCode'}, inplace=True) # Rename the numeric one back

    # Final check of column types (optional, but good for verification)
    print("\nDataFrame info after StockCode cleaning and type conversion:")
    df.info()

    # Save cleaned data
    df.to_excel(output_file, index=False)
    print(f"Saved cleaned data to '{output_file}' ({len(df)} rows) after dropping {initial_rows - len(df)} total rows.")
    return df

# Example usage
# IMPORTANT: Use your original input file and specify a new output file name
clean_stockcodes(
    input_file='OnlineRetail.xlsx', # Make sure this is the original, unprocessed file
    output_file='Cleaned_OnlineRetail_ForBI.xlsx' # Save to a NEW file
)