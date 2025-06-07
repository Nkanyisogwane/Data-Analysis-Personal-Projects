import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
server = 'UGWANE'
database = 'OnlineRetailStarSchema'
conn_str = f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# CSV file paths (update these with your actual paths)
csv_files = {
    'dim_country': 'dim_country.csv',
    'dim_customer': 'dim_customer.csv',
    'dim_date': 'dim_date.csv',
    'dim_product': 'dim_product.csv',
    'fact_sales': 'fact_sales.csv'
}

def import_csv_to_sql(csv_path, table_name, engine):
    """Import a CSV file to SQL Server table"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Write to SQL Server
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Successfully imported {len(df)} rows to {table_name}")
        
    except Exception as e:
        print(f"Error importing {table_name}: {str(e)}")

def main():
    try:
        # Create SQLAlchemy engine
        engine = create_engine(conn_str)
        print("Connected to SQL Server successfully")
        
        # Import each CSV file
        for table_name, csv_path in csv_files.items():
            import_csv_to_sql(csv_path, table_name, engine)
            
    except Exception as e:
        print(f"Database connection error: {str(e)}")
    finally:
        if 'engine' in locals():
            engine.dispose()
            print("Connection closed")

if __name__ == "__main__":
    main()