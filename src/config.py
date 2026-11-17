
from pathlib import Path

# Main project folder
ROOT = Path(__file__).resolve().parents[1]

# Dataset folders
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

# Create folders if they do not exist
for folder in [RAW, PROCESSED, OUTPUTS]:
    folder.mkdir(parents=True, exist_ok=True)

# Dataset filenames
FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "translation": "product_category_name_translation.csv"
}

def get_file(key):
    if key not in FILES:
        raise ValueError("Invalid dataset name: " + key)

    path = RAW / FILES[key]

    if not path.exists():
        raise FileNotFoundError(
            "Dataset file not found: " + str(path)
        )

    return path
