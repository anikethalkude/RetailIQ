
import pandas as pd
import json
from pathlib import Path

# Project location
ROOT = Path(__file__).resolve().parents[1]

# Dataset location
RAW_FOLDER = ROOT / "data" / "raw"
OUTPUT_FOLDER = ROOT / "outputs"

# Create output folder if it does not exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Dataset files
files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

report = {}

print("\n========== RETAILIQ DATA QUALITY REPORT ==========\n")

for file in files:

    file_path = RAW_FOLDER / file

    if not file_path.exists():
        print(f"FILE NOT FOUND: {file}")
        continue

    # Read dataset
    df = pd.read_csv(file_path)

    # Basic information
    rows, columns = df.shape

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    print(f"Dataset: {file}")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")
    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print("-" * 50)

    # Store report
    report[file] = {
        "rows": int(rows),
        "columns": int(columns),
        "column_names": df.columns.tolist(),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows
    }

# Save report
report_path = OUTPUT_FOLDER / "data_quality_report.json"

with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4)

print("\nData profiling completed!")
print(f"Report saved at: {report_path}")
