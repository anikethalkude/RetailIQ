
import pandas as pd
from src.config import PROCESSED

# Load monthly demand data
file_path = PROCESSED / "monthly_category_demand.csv"

df = pd.read_csv(file_path)

# Convert month column into datetime
df["purchase_month"] = pd.to_datetime(
    df["purchase_month"]
)

print("\n========== RETAILIQ DEMAND ANALYSIS ==========\n")

# 1. Dataset information
print("Total records:", len(df))

print(
    "Date range:",
    df["purchase_month"].min().date(),
    "to",
    df["purchase_month"].max().date()
)

print(
    "Total product categories:",
    df["product_category_name_english"].nunique()
)

# 2. Find top 10 categories by demand
category_summary = (
    df.groupby("product_category_name_english")
    .agg(
        total_demand=("order_item_count", "sum"),
        total_revenue=("revenue", "sum"),
        active_months=("purchase_month", "nunique")
    )
    .sort_values("total_demand", ascending=False)
)

print("\nTOP 10 PRODUCT CATEGORIES BY DEMAND:\n")
print(category_summary.head(10).to_string())

# 3. Check monthly data availability
print("\nMONTHLY DATA AVAILABILITY:\n")

print(
    df.groupby("product_category_name_english")
    ["purchase_month"]
    .nunique()
    .describe()
)

# 4. Save category summary
output_file = PROCESSED / "category_summary.csv"

category_summary.to_csv(output_file)

print("\nCategory summary saved successfully!")
print("File:", output_file)

print("\n========== ANALYSIS COMPLETED ==========")
