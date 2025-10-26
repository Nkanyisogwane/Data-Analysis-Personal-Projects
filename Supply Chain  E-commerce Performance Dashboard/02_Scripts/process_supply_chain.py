import pandas as pd

def set_supply_chain_datatypes(file_path):
    """
    Loads the DataCoSupplyChainDataset from a CSV file and sets appropriate data types.

    Args:
        file_path (str): The path to your DataCoSupplyChainDataset CSV file.

    Returns:
        pandas.DataFrame: The DataFrame with adjusted data types.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path, encoding='latin1', parse_dates=['shipping date (DateOrders)', 'order date (DateOrders)'])
        # You might need to adjust 'encoding' based on your file. 'utf-8' is common, 'latin1' or 'ISO-8859-1' are also possibilities.

        print(f"Successfully loaded {file_path}. Initial shape: {df.shape}")
        print("Inferring and setting data types...")

        # --- Numerical Columns (Integers and Decimals) ---
        numerical_int_cols = [
            'Product Status', 'Product Card Id', 'Product Category Id',
            'Order Item Quantity', 'Order Item Cardprod Id', 'Order Item Id',
            'Order Customer Id', 'Order Id', 'Department Id', 'Customer Id',
            'Late_delivery_risk', 'Category Id', 'Days for shipping (real)',
            'Days for shipment (scheduled)'
        ]
        for col in numerical_int_cols:
            if col in df.columns:
                # Use pd.to_numeric with errors='coerce' to turn unparseable values into NaN
                # Then, convert to Int64 (nullable integer) to handle NaNs if any
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            else:
                print(f"Warning: Column '{col}' not found in the dataset.")

        numerical_float_cols = [
            'Product Price', 'Order Item Profit Ratio', 'Sales',
            'Order Item Total', 'Order Profit Per Order', 'Order Item Discount',
            'Order Item Discount Rate', 'Order Item Product Price',
            'Latitude', 'Longitude', 'Benefit per order', 'Sales per customer'
        ]
        for col in numerical_float_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce') # Default to float64, handles NaNs
            else:
                print(f"Warning: Column '{col}' not found in the dataset.")

        # --- Date/Time Columns ---
        # Already handled in pd.read_csv parse_dates for specified columns.
        # Ensure they are datetime objects, Power BI will recognize this.
        date_cols = ['shipping date (DateOrders)', 'order date (DateOrders)']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            else:
                print(f"Warning: Date column '{col}' not found in the dataset.")


        # --- Text/Categorical Columns ---
        # Iterate through remaining columns and set to 'object' (string) or 'category'
        # 'category' is memory efficient for columns with limited unique values.
        for col in df.columns:
            if col not in numerical_int_cols + numerical_float_cols + date_cols:
                # Check for high cardinality before converting to 'category'
                # A good threshold for categorical columns is subjective,
                # but typically less than 50% unique values, or a fixed number like < 100.
                if df[col].nunique() < df.shape[0] * 0.5 and df[col].dtype == 'object':
                    df[col] = df[col].astype('category')
                else:
                    df[col] = df[col].astype(str) # Ensure all others are strings

        # --- Special Handling / Data Quality Notes ---
        if 'Product Description' in df.columns:
            # Your observation: "Has 100% empty, so may need to be excluded or its source investigated."
            if df['Product Description'].isnull().all() or (df['Product Description'] == '').all():
                print("Note: 'Product Description' is entirely empty/null. Consider dropping or investigating source.")

        if 'Order Zipcode' in df.columns:
            # Your observation: "Has 97% empty/null values."
            print("Note: 'Order Zipcode' has a high percentage of empty/null values. Address data quality if crucial for analysis.")
            df['Order Zipcode'] = df['Order Zipcode'].astype(str) # Keep as string for potential leading zeros

        if 'Customer Zipcode' in df.columns:
            print("Note: 'Customer Zipcode' has a high percentage of empty/null values. Address data quality if crucial for analysis.")
            df['Customer Zipcode'] = df['Customer Zipcode'].astype(str) # Keep as string for potential leading zeros

        # --- Sensitive Data Handling ---
        if 'Customer Password' in df.columns:
            print("\nWARNING: 'Customer Password' column detected.")
            print("         Consider dropping this column or masking its contents before importing into Power BI for security reasons.")
            # Example to drop: df = df.drop(columns=['Customer Password'])
            # Example to mask: df['Customer Password'] = '********'

        if 'Customer Email' in df.columns:
            print("WARNING: 'Customer Email' column detected.")
            print("         Consider dropping this column or masking its contents before importing into Power BI for privacy reasons.")
            # Example to drop: df = df.drop(columns=['Customer Email'])
            # Example to mask: df['Customer Email'] = df['Customer Email'].apply(lambda x: '***@***.com' if pd.notnull(x) else x)

        # Confirming potential duplicate IDs
        if 'Customer Id' in df.columns and 'Order Customer Id' in df.columns:
            if df['Customer Id'].equals(df['Order Customer Id']):
                print("Observation: 'Customer Id' and 'Order Customer Id' appear to be identical. You might only need one.")
            else:
                print("Observation: 'Customer Id' and 'Order Customer Id' are present and different. Keep both if they represent distinct IDs.")

        if 'Category Id' in df.columns and 'Product Category Id' in df.columns:
            if df['Category Id'].equals(df['Product Category Id']):
                print("Observation: 'Category Id' and 'Product Category Id' appear to be identical. You might only need one.")
            else:
                print("Observation: 'Category Id' and 'Product Category Id' are present and different. Keep both if they represent distinct IDs.")


        print("\nData type setting complete.")
        print("\nFinal DataFrame Info:")
        df.info()

        return df

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the path.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- How to use the script ---
if __name__ == "__main__":
    # IMPORTANT: Replace 'path/to/your/DataCoSupplyChainDataset.csv' with the actual path to your CSV file
    csv_file_path = 'DataCoSupplyChainDataset.csv' # Assuming it's in the same directory as your script

    processed_df = set_supply_chain_datatypes(csv_file_path)

    # Corrected indentation for the final if block
    if processed_df is not None:
        # Save the processed DataFrame to a new CSV file
        processed_df.to_csv('DataCoSupplyChainDataset_cleaned.csv', index=False)
        print("\nCleaned data saved to 'DataCoSupplyChainDataset_cleaned.csv'")
        print("You can now import 'DataCoSupplyChainDataset_cleaned.csv' into Power BI.")
        print("Remember to review the 'Sensitive Data Handling' warnings.")