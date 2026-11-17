
import pandas as pd
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
from pathlib import Path
import os

# Load database credentials
load_dotenv()

# Create PostgreSQL connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(connection_url)

# Location of processed CSV files
processed_folder = Path("data/processed")

# CSV filename : PostgreSQL table name
tables = {
    "fact_orders.csv": "fact_orders",
    "fact_order_items.csv": "fact_order_items",
    "dim_customers.csv": "dim_customers",
    "dim_products.csv": "dim_products",
    "monthly_category_demand.csv": "monthly_category_demand"
}

print("\n========== RETAILIQ DATABASE IMPORT ==========\n")

try:
    for filename, table_name in tables.items():

        file_path = processed_folder / filename

        print(f"Importing {filename}...")

        # Read CSV
        df = pd.read_csv(file_path)

        # Convert date columns into proper datetime values
        date_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "purchase_month"
        ]

        for column in date_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column], errors="coerce"
                )

        # Import into PostgreSQL
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=5000
        )

        print(f"Successfully imported {len(df)} rows.")

    print("\n========== IMPORT VERIFICATION ==========\n")

    # Verify each database table
    with engine.connect() as connection:

        for table_name in tables.values():

            result = connection.execute(
                text(f'SELECT COUNT(*) FROM "{table_name}"')
            )

            count = result.scalar()

            print(f"{table_name}: {count} rows")

    print("\nALL DATASETS IMPORTED SUCCESSFULLY!")

except Exception as error:
    print("\nDATABASE IMPORT FAILED!")
    print("Error:", error)

finally:
    engine.dispose()
