
import pandas as pd
import matplotlib.pyplot as plt

from src.config import PROCESSED, OUTPUTS

print("\n========== RETAILIQ VISUALIZATION ==========\n")

# Load datasets
historical = pd.read_csv(
    PROCESSED / "monthly_category_demand.csv"
)

predictions = pd.read_csv(
    OUTPUTS / "forecast_predictions.csv"
)

future = pd.read_csv(
    OUTPUTS / "future_demand_forecast.csv"
)

# Convert dates
historical["purchase_month"] = pd.to_datetime(
    historical["purchase_month"]
)

predictions["month"] = pd.to_datetime(
    predictions["month"]
)

future["month"] = pd.to_datetime(
    future["month"]
)

# Select top five categories
top_categories = (
    historical.groupby("product_category_name_english")
    ["order_item_count"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index.tolist()
)

OUTPUTS.mkdir(exist_ok=True)

# ------------------------------------------------
# CHART 1: HISTORICAL MONTHLY DEMAND
# ------------------------------------------------

plt.figure(figsize=(12, 6))

for category in top_categories:

    category_data = historical[
        historical["product_category_name_english"] == category
    ]

    monthly = (
        category_data.groupby("purchase_month")
        ["order_item_count"]
        .sum()
        .sort_index()
    )

    plt.plot(
        monthly.index,
        monthly.values,
        marker="o",
        label=category
    )

plt.title("Historical Monthly Product Demand")
plt.xlabel("Month")
plt.ylabel("Number of Order Items")
plt.legend()
plt.grid(True)
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    OUTPUTS / "historical_demand.png",
    dpi=300
)

plt.show()


# ------------------------------------------------
# CHART 2: ACTUAL VS RANDOM FOREST PREDICTIONS
# ------------------------------------------------

comparison = (
    predictions.groupby("category")
    [["actual_demand", "random_forest_prediction"]]
    .sum()
)

comparison = comparison.reindex(top_categories)

positions = range(len(comparison))
width = 0.35

plt.figure(figsize=(12, 6))

plt.bar(
    [p - width / 2 for p in positions],
    comparison["actual_demand"],
    width=width,
    label="Actual Demand"
)

plt.bar(
    [p + width / 2 for p in positions],
    comparison["random_forest_prediction"],
    width=width,
    label="Random Forest Prediction"
)

plt.title("Actual vs Predicted Demand (Test Period)")
plt.xlabel("Product Category")
plt.ylabel("Total Order Items")
plt.xticks(
    list(positions),
    comparison.index,
    rotation=25,
    ha="right"
)

plt.legend()
plt.grid(axis="y")
plt.tight_layout()

plt.savefig(
    OUTPUTS / "actual_vs_predicted.png",
    dpi=300
)

plt.show()


# ------------------------------------------------
# CHART 3: FUTURE DEMAND FORECAST
# ------------------------------------------------

forecast_pivot = future.pivot(
    index="month",
    columns="category",
    values="predicted_demand"
)

plt.figure(figsize=(12, 6))

for category in forecast_pivot.columns:

    plt.plot(
        forecast_pivot.index,
        forecast_pivot[category],
        marker="o",
        label=category
    )

plt.title("Future Monthly Demand Forecast (2018)")
plt.xlabel("Forecast Month")
plt.ylabel("Predicted Order Items")
plt.legend()
plt.grid(True)
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    OUTPUTS / "future_demand_chart.png",
    dpi=300
)

plt.show()


print("\nAll charts generated successfully!")

print("\nSaved files:")
print("outputs/historical_demand.png")
print("outputs/actual_vs_predicted.png")
print("outputs/future_demand_chart.png")

print("\n========== VISUALIZATION COMPLETED ==========")
