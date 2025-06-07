import pandas as pd
import os

def export_excel_to_csv(excel_files, output_directory="."):
    """
    Reads a list of Excel files and exports each sheet within them to a CSV file.
    The CSV file will have the same name as the Excel file (with a .csv extension).

    Args:
        excel_files (list): A list of strings, where each string is the name
                            of an Excel file (e.g., ['file1.xlsx', 'file2.xlsx']).
        output_directory (str): The directory where the CSV files will be saved.
                                Defaults to the current directory.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    for excel_file in excel_files:
        try:
            # Construct the full path to the Excel file
            excel_path = os.path.join(output_directory, excel_file)

            # Read the Excel file into a pandas DataFrame
            # header=0 means the first row is used as column names
            df = pd.read_excel(excel_path, header=0)

            # Construct the output CSV file name
            # Replace .xlsx or .xls with .csv
            csv_file = os.path.splitext(excel_file)[0] + '.csv'
            csv_path = os.path.join(output_directory, csv_file)

            # Export the DataFrame to a CSV file
            # index=False prevents pandas from writing the DataFrame index as a column in the CSV
            df.to_csv(csv_path, index=False)
            print(f"Successfully exported '{excel_file}' to '{csv_file}'")

        except FileNotFoundError:
            print(f"Error: Excel file '{excel_file}' not found. Please ensure it's in the '{output_directory}' directory.")
        except Exception as e:
            print(f"An error occurred while processing '{excel_file}': {e}")

# --- List of your Excel files to convert ---
# Make sure these Excel files are in the same directory as this Python script,
# or provide their full path.
excel_files_to_convert = [
    'dim_country.xlsx',
    'dim_customer.xlsx',
    'dim_date.xlsx',
    'dim_product.xlsx',
    'fact_sales.xlsx'
]

# --- Run the conversion ---
# By default, CSVs will be saved in the same directory as the script.
# If your Excel files are in a different folder, update `current_directory` or `excel_files_to_convert`
current_directory = os.getcwd()
export_excel_to_csv(excel_files_to_convert, output_directory=current_directory)

print("\nConversion process complete.")
print("You should now find your CSV files in the same folder as this script.")
