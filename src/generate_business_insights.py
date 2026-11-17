
from pathlib import Path
import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

OUTPUTS.mkdir(exist_ok=True)

# Load existing analytical results
monthly = pd.read_csv(
    PROCESSED / "monthly_category_demand.csv"
)

metrics = pd.read_csv(
    OUTPUTS / "forecast_metrics.csv"
)

future = pd.read_csv(
    OUTPUTS / "future_demand_forecast.csv"
)

# Convert date columns
monthly["purchase_month"] = pd.to_datetime(
    monthly["purchase_month"]
)

future["month"] = pd.to_datetime(future["month"])

insights = []
recommendations = []

# ------------------------------------------------
# 1. CATEGORY PERFORMANCE
# ------------------------------------------------

category_performance = (
    monthly.groupby("product_category_name_english")
    .agg(
        total_demand=("order_item_count", "sum"),
        total_revenue=("revenue", "sum")
    )
    .reset_index()
)

top_demand = category_performance.nlargest(
    1, "total_demand"
).iloc[0]

top_revenue = category_performance.nlargest(
    1, "total_revenue"
).iloc[0]

insights.append(
    f"Highest demand category: "
    f"{top_demand['product_category_name_english']} "
    f"with {top_demand['total_demand']:,.0f} items."
)

insights.append(
    f"Highest revenue category: "
    f"{top_revenue['product_category_name_english']} "
    f"with revenue of {top_revenue['total_revenue']:,.2f}."
)

recommendations.append(
    f"Prioritize demand planning and inventory review "
    f"for {top_demand['product_category_name_english']}."
)

# ------------------------------------------------
# 2. MONTHLY DEMAND TREND
# ------------------------------------------------

monthly_trend = (
    monthly.groupby("purchase_month")["order_item_count"]
    .sum()
    .sort_index()
)

if len(monthly_trend) >= 2:

    latest = monthly_trend.iloc[-1]
    previous = monthly_trend.iloc[-2]

    if previous > 0:

        change = ((latest - previous) / previous) * 100

        insights.append(
            f"Latest historical monthly demand changed "
            f"by {change:.2f}% compared with the previous month."
        )

        if change > 0:
            recommendations.append(
                "Review recent demand growth when planning "
                "future inventory."
            )
        elif change < 0:
            recommendations.append(
                "Investigate the recent demand decline "
                "before adjusting inventory."
            )
        else:
            recommendations.append(
                "Monitor demand because the latest monthly "
                "demand is unchanged."
            )

# ------------------------------------------------
# 3. FUTURE DEMAND FORECAST
# ------------------------------------------------

forecast_monthly = (
    future.groupby("month")["predicted_demand"]
    .sum()
    .sort_index()
)

forecast_total = future["predicted_demand"].sum()

insights.append(
    f"Total projected demand across the forecast period: "
    f"{forecast_total:,.0f} items."
)

for month, demand in forecast_monthly.items():

    insights.append(
        f"Projected demand for {month.strftime('%B %Y')}: "
        f"{demand:,.0f} items."
    )

forecast_category = (
    future.groupby("category")["predicted_demand"]
    .sum()
    .sort_values(ascending=False)
)

if not forecast_category.empty:

    top_forecast = forecast_category.index[0]

    recommendations.append(
        f"Monitor forecast demand for {top_forecast}, "
        f"which has the highest projected demand."
    )

# ------------------------------------------------
# 4. MACHINE LEARNING MODEL EVALUATION
# ------------------------------------------------

rf_wins = (
    metrics["random_forest_mae"] <
    metrics["baseline_mae"]
).sum()

baseline_wins = (
    metrics["baseline_mae"] <
    metrics["random_forest_mae"]
).sum()

avg_rf_mae = metrics["random_forest_mae"].mean()
avg_baseline_mae = metrics["baseline_mae"].mean()

insights.append(
    f"Random Forest has lower MAE in {rf_wins} "
    f"out of {len(metrics)} categories."
)

insights.append(
    f"Baseline has lower MAE in {baseline_wins} "
    f"out of {len(metrics)} categories."
)

insights.append(
    f"Average Random Forest MAE: {avg_rf_mae:.2f}."
)

insights.append(
    f"Average Baseline MAE: {avg_baseline_mae:.2f}."
)

if avg_rf_mae < avg_baseline_mae:

    recommendations.append(
        "Random Forest has lower average MAE. "
        "Continue evaluating it before selecting it "
        "for production forecasting."
    )

elif avg_baseline_mae < avg_rf_mae:

    recommendations.append(
        "The baseline has lower average MAE. "
        "Do not replace the baseline with Random Forest "
        "without further validation."
    )

else:

    recommendations.append(
        "Both methods have equal average MAE. "
        "Compare their category-level performance."
    )

# ------------------------------------------------
# 5. GENERATE BUSINESS INSIGHTS REPORT
# ------------------------------------------------

report = []

report.append("=" * 55)
report.append("RETAILIQ - AI BUSINESS INSIGHTS ENGINE")
report.append("=" * 55)

report.append("\n1. CATEGORY PERFORMANCE")

for item in insights[:2]:
    report.append("- " + item)

report.append("\n2. HISTORICAL DEMAND")

for item in insights[2:3]:
    report.append("- " + item)

report.append("\n3. FUTURE DEMAND FORECAST")

for item in insights[3:3 + len(forecast_monthly)]:
    report.append("- " + item)

report.append("\n4. MODEL PERFORMANCE")

for item in insights[3 + len(forecast_monthly):]:
    report.append("- " + item)

report.append("\n5. BUSINESS RECOMMENDATIONS")

for item in recommendations:
    report.append("- " + item)

report.append("\n" + "=" * 55)
report.append("END OF RETAILIQ BUSINESS INSIGHTS")
report.append("=" * 55)

# Save report
output_file = OUTPUTS / "business_insights.txt"

output_file.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print("\n".join(report))

print("\nBusiness insights saved successfully!")
print(f"Report location: {output_file}")
