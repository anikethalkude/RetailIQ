
import pandas as pd
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from src.config import ROOT, OUTPUTS

print("\n========== RETAILIQ POSTGRESQL FORECAST UPLOAD ==========\n")

# Load database credentials from .env
load_dotenv(ROOT / ".env")

# Create PostgreSQL connection securely
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(database_url)

# Files and corresponding PostgreSQL table names
datasets = {
    "forecast_metrics": OUTPUTS / "forecast_metrics.csv",
    "forecast_predictions": OUTPUTS / "forecast_predictions.csv",
    "future_demand_forecast": OUTPUTS / "future_demand_forecast.csv"
}

for table_name, file_path in datasets.items():

    print(f"\nUploading: {table_name}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load dates correctly
    if table_name == "forecast_predictions":
        df = pd.read_csv(file_path, parse_dates=["month"])

    elif table_name == "future_demand_forecast":
        df = pd.read_csv(file_path, parse_dates=["month"])

    else:
        df = pd.read_csv(file_path)

    # Upload data to PostgreSQL
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Rows uploaded:", len(df))
    print("Upload successful!")

# Verify uploaded tables
print("\n========== DATABASE VERIFICATION ==========\n")

with engine.connect() as connection:

    for table_name in datasets:

        result = pd.read_sql(
            f'SELECT COUNT(*) AS total_rows FROM "{table_name}"',
            connection
        )

        print(
            table_name,
            "->",
            result.iloc[0]["total_rows"],
            "records"
        )

engine.dispose()

print("\nALL FORECAST DATA UPLOADED SUCCESSFULLY!")
