
import pandas as pd
from src.config import get_file, PROCESSED

print("\n========== RETAILIQ DATA PREPROCESSING ==========\n")

# 1. Load all required datasets
orders = pd.read_csv(get_file("orders"))
items = pd.read_csv(get_file("items"))
customers = pd.read_csv(get_file("customers"))
products = pd.read_csv(get_file("products"))
payments = pd.read_csv(get_file("payments"))
reviews = pd.read_csv(get_file("reviews"))
translation = pd.read_csv(get_file("translation"))

print("All datasets loaded successfully.")

# 2. Remove exact duplicate rows
datasets = [
    orders, items, customers, products,
    payments, reviews, translation
]

for df in datasets:
    df.drop_duplicates(inplace=True)

# 3. Convert order date columns into date format
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column], errors="coerce"
    )

# 4. Translate product categories into English
products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

products["product_category_name_english"] = (
    products["product_category_name_english"]
    .fillna(products["product_category_name"])
    .fillna("unknown")
)

# 5. Create a clean customer dimension
dim_customers = customers.drop_duplicates(
    subset=["customer_id"]
).copy()

# 6. Create a clean product dimension
dim_products = products.drop_duplicates(
    subset=["product_id"]
).copy()

# 7. Aggregate payment data at order level
payment_summary = payments.groupby("order_id").agg(
    total_payment=("payment_value", "sum"),
    payment_types=("payment_type", "nunique")
).reset_index()

# 8. Aggregate review data at order level
review_summary = reviews.groupby("order_id").agg(
    average_review_score=("review_score", "mean"),
    review_count=("review_score", "count")
).reset_index()

# 9. Create one row per order
fact_orders = orders.merge(
    payment_summary,
    on="order_id",
    how="left"
)

fact_orders = fact_orders.merge(
    review_summary,
    on="order_id",
    how="left"
)

# 10. Prepare order information for item-level analysis
order_columns = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

fact_order_items = items.merge(
    orders[order_columns],
    on="order_id",
    how="left"
)

# Add product information
product_columns = [
    "product_id",
    "product_category_name_english"
]

fact_order_items = fact_order_items.merge(
    products[product_columns],
    on="product_id",
    how="left"
)

# Add customer information
customer_columns = [
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
]

fact_order_items = fact_order_items.merge(
    customers[customer_columns],
    on="customer_id",
    how="left"
)

fact_order_items["product_category_name_english"] = (
    fact_order_items["product_category_name_english"]
    .fillna("unknown")
)

# 11. Create monthly category-level demand data
monthly_data = fact_order_items.dropna(
    subset=["order_purchase_timestamp"]
).copy()

monthly_data["purchase_month"] = (
    monthly_data["order_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly_category_demand = (
    monthly_data.groupby(
        ["purchase_month", "product_category_name_english"]
    )
    .agg(
        order_item_count=("order_item_id", "count"),
        revenue=("price", "sum"),
        freight_value=("freight_value", "sum"),
        unique_orders=("order_id", "nunique")
    )
    .reset_index()
)

# 12. Save all processed datasets
output_tables = {
    "fact_orders.csv": fact_orders,
    "fact_order_items.csv": fact_order_items,
    "dim_customers.csv": dim_customers,
    "dim_products.csv": dim_products,
    "monthly_category_demand.csv": monthly_category_demand
}

for filename, dataframe in output_tables.items():
    dataframe.to_csv(
        PROCESSED / filename,
        index=False
    )

    print(
        f"Saved {filename}: "
        f"{len(dataframe)} rows"
    )

print("\n========== PREPROCESSING COMPLETED ==========")
print("Processed files saved in:", PROCESSED)
