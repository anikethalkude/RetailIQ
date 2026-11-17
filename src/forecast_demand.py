
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import PROCESSED

print("\n========== RETAILIQ DEMAND FORECASTING ==========\n")

# 1. Load monthly demand dataset
file_path = PROCESSED / "monthly_category_demand.csv"
df = pd.read_csv(file_path)

df["purchase_month"] = pd.to_datetime(df["purchase_month"])

# 2. Select top five categories by demand
top_categories = (
    df.groupby("product_category_name_english")
    ["order_item_count"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index.tolist()
)

print("Selected categories:")
for category in top_categories:
    print("-", category)

# 3. Create output folders
Path("outputs").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)

metrics_results = []
all_predictions = []
trained_models = {}

# 4. Train a separate model for each category
for category in top_categories:

    print(f"\nTraining model: {category}")

    category_data = df[
        df["product_category_name_english"] == category
    ].copy()

    # Aggregate monthly demand
    monthly = (
        category_data.groupby("purchase_month")
        ["order_item_count"]
        .sum()
        .sort_index()
    )

    # Fill months without recorded sales with zero
    full_months = pd.date_range(
        start=df["purchase_month"].min(),
        end=df["purchase_month"].max(),
        freq="MS"
    )

    monthly = monthly.reindex(
        full_months,
        fill_value=0
    )

    # 5. Create previous-month features
    features = pd.DataFrame(index=monthly.index)

    features["lag_1"] = monthly.shift(1)
    features["lag_2"] = monthly.shift(2)
    features["lag_3"] = monthly.shift(3)

    features["rolling_mean_3"] = (
        monthly.shift(1)
        .rolling(window=3)
        .mean()
    )

    features["month"] = monthly.index.month

    features["actual_demand"] = monthly

    features = features.dropna()

    # 6. Chronological train-test split
    # Last four months are reserved for testing
    train = features.iloc[:-4]
    test = features.iloc[-4:]

    X_train = train.drop(columns=["actual_demand"])
    y_train = train["actual_demand"]

    X_test = test.drop(columns=["actual_demand"])
    y_test = test["actual_demand"]

    # 7. Train Random Forest
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=4,
        min_samples_leaf=2,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Demand cannot be negative
    predictions = np.maximum(predictions, 0)

    # 8. Baseline: previous month's demand
    baseline_predictions = X_test["lag_1"].values

    # 9. Calculate evaluation metrics
    model_mae = mean_absolute_error(
        y_test, predictions
    )

    model_rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    baseline_mae = mean_absolute_error(
        y_test, baseline_predictions
    )

    baseline_rmse = np.sqrt(
        mean_squared_error(y_test, baseline_predictions)
    )

    # 10. Save metrics
    metrics_results.append({
        "category": category,
        "training_months": len(train),
        "testing_months": len(test),
        "random_forest_mae": round(model_mae, 2),
        "random_forest_rmse": round(model_rmse, 2),
        "baseline_mae": round(baseline_mae, 2),
        "baseline_rmse": round(baseline_rmse, 2)
    })

    # 11. Save predictions
    prediction_df = pd.DataFrame({
        "month": test.index,
        "category": category,
        "actual_demand": y_test.values,
        "random_forest_prediction": predictions.round(2),
        "baseline_prediction": baseline_predictions
    })

    all_predictions.append(prediction_df)

    # Store trained model
    trained_models[category] = model

    print("Training records:", len(train))
    print("Testing records:", len(test))
    print("Random Forest MAE:", round(model_mae, 2))
    print("Baseline MAE:", round(baseline_mae, 2))

# 12. Save evaluation results
metrics_df = pd.DataFrame(metrics_results)

metrics_df.to_csv(
    "outputs/forecast_metrics.csv",
    index=False
)

predictions_df = pd.concat(
    all_predictions,
    ignore_index=True
)

predictions_df.to_csv(
    "outputs/forecast_predictions.csv",
    index=False
)

# 13. Save trained models
joblib.dump(
    trained_models,
    "models/demand_forecasting_models.pkl"
)

print("\n========== FINAL MODEL COMPARISON ==========\n")
print(metrics_df.to_string(index=False))

print("\nFiles saved successfully:")
print("outputs/forecast_metrics.csv")
print("outputs/forecast_predictions.csv")
print("models/demand_forecasting_models.pkl")

print("\n========== FORECASTING COMPLETED ==========")
