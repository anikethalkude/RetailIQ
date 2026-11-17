
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from src.config import PROCESSED, OUTPUTS

print("\n========== RETAILIQ FUTURE DEMAND FORECAST ==========\n")

# Load historical demand and model evaluation results
df = pd.read_csv(PROCESSED / "monthly_category_demand.csv")
metrics = pd.read_csv(OUTPUTS / "forecast_metrics.csv")

df["purchase_month"] = pd.to_datetime(df["purchase_month"])

# Select the same top five categories
top_categories = (
    df.groupby("product_category_name_english")["order_item_count"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index.tolist()
)

future_results = []

for category in top_categories:

    print(f"\nForecasting: {category}")

    category_data = df[
        df["product_category_name_english"] == category
    ].copy()

    monthly = (
        category_data.groupby("purchase_month")["order_item_count"]
        .sum()
        .sort_index()
    )

    # Include months with zero recorded demand
    full_months = pd.date_range(
        start=df["purchase_month"].min(),
        end=df["purchase_month"].max(),
        freq="MS"
    )

    monthly = monthly.reindex(full_months, fill_value=0)

    # Create historical features
    features = pd.DataFrame(index=monthly.index)

    features["lag_1"] = monthly.shift(1)
    features["lag_2"] = monthly.shift(2)
    features["lag_3"] = monthly.shift(3)

    features["rolling_mean_3"] = (
        monthly.shift(1).rolling(3).mean()
    )

    features["month"] = monthly.index.month
    features["actual_demand"] = monthly

    training_data = features.dropna()

    X_train = training_data.drop(columns=["actual_demand"])
    y_train = training_data["actual_demand"]

    # Select the method with lower test MAE
    result = metrics[metrics["category"] == category].iloc[0]

    use_random_forest = (
        result["random_forest_mae"] <= result["baseline_mae"]
    )

    method = "Random Forest" if use_random_forest else "3-Month Moving Average"

    if use_random_forest:

        # Retrain using all available historical records
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=4,
            min_samples_leaf=2,
            random_state=42
        )

        model.fit(X_train, y_train)

    # Generate three future monthly predictions
    history = list(monthly.values)

    future_months = pd.date_range(
        start=monthly.index.max() + pd.offsets.MonthBegin(1),
        periods=3,
        freq="MS"
    )

    for future_month in future_months:

        if use_random_forest:

            input_data = pd.DataFrame([{
                "lag_1": history[-1],
                "lag_2": history[-2],
                "lag_3": history[-3],
                "rolling_mean_3": np.mean(history[-3:]),
                "month": future_month.month
            }])

            prediction = model.predict(input_data)[0]

        else:
    # Use the average demand from the previous three months
            prediction = np.mean(history[-3:])

        prediction = max(0, round(float(prediction), 2))

        future_results.append({
            "month": future_month,
            "category": category,
            "predicted_demand": prediction,
            "selected_method": method
        })

        history.append(prediction)

    print("Selected method:", method)

# Save all forecasts
forecast_df = pd.DataFrame(future_results)

OUTPUTS.mkdir(parents=True, exist_ok=True)

forecast_df.to_csv(
    OUTPUTS / "future_demand_forecast.csv",
    index=False
)

print("\n========== FUTURE FORECAST RESULTS ==========\n")
print(forecast_df.to_string(index=False))

print("\nSaved: outputs/future_demand_forecast.csv")
print("\n========== FORECASTING COMPLETED ==========")
