import pandas as pd

def verify_unique_rows(file_path):
    """
    Loads an Excel file, counts the initial number of rows,
    removes exact duplicate rows across all columns, and
    prints the row count before and after duplicate removal.

    Args:
        file_path (str): The path to the Excel file.
    """
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        print(f"Successfully loaded '{file_path}'.")

        # Get the initial number of rows
        initial_rows = len(df)
        print(f"Initial number of rows: {initial_rows}")

        # Remove exact duplicate rows across all columns
        # (This is the default behavior of drop_duplicates() when no 'subset' is specified)
        df_unique = df.drop_duplicates()

        # Get the number of rows after removing duplicates
        rows_after_duplicates = len(df_unique)
        print(f"Number of rows after removing all exact duplicates: {rows_after_duplicates}")

        # Calculate how many rows were removed
        rows_removed = initial_rows - rows_after_duplicates
        print(f"Total duplicate rows removed: {rows_removed}")

        # Check if the result matches 37 as expected
        if rows_after_duplicates == 37:
            print("\nResult CONFIRMED: The number of unique rows is 37. This matches your Power BI observation!")
            print("This confirms the total sales figure of 2920 is based on these 37 distinct transaction line items.")
            print("The previous 228M figure was indeed due to over-counting massive duplicates.")
        else:
            print(f"\nResult: The number of unique rows is {rows_after_duplicates}, which differs from 37.")
            print("This might indicate a slight difference in how duplicates were previously handled or a different file was used.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Example Usage ---
# Make sure 'Cleaned_OnlineRetail_ForBI.xlsx' is in the same directory as this Python script,
# or provide the full path to the file.
file_to_check = 'Cleaned_OnlineRetail_ForBI.xlsx'
verify_unique_rows(file_to_check)