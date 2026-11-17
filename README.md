# RetailIQ – AI-Powered Retail Intelligence & Demand Forecasting Platform

## Project Overview

RetailIQ is an end-to-end retail analytics and demand forecasting platform built using Python, PostgreSQL, Machine Learning, and Power BI.

The project analyzes historical e-commerce transactions to identify business trends, understand customer and operational performance, forecast product-category demand, and generate data-driven business insights.

It transforms raw retail data into structured datasets, analytical SQL queries, forecasting outputs, and interactive business dashboards.

## Project Objectives

- Analyze historical retail sales and transaction data.
- Identify high-performing product categories.
- Measure revenue trends and customer purchasing patterns.
- Analyze delivery and operational performance.
- Develop and evaluate demand forecasting models.
- Store and analyze structured data using PostgreSQL.
- Present business insights through Power BI.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn, Random Forest |
| Database | PostgreSQL |
| SQL Analytics | CTEs, Window Functions, Joins, Aggregations |
| Business Intelligence | Power BI, DAX |
| Development | VS Code, Git, GitHub |

## Dataset

This project uses the Brazilian E-Commerce Public Dataset by Olist, available on Kaggle.

Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains historical e-commerce information, including orders, customers, products, sellers, payments, and reviews.

**Important:** The dataset represents historical transactions, primarily from 2016–2018. Forecasts are experimental projections based on this historical data, not live market predictions.

## Project Architecture

1. **Data Collection:** Load the original Olist CSV datasets.
2. **Data Preparation:** Clean, transform, and prepare analytical datasets using Python.
3. **Data Analysis:** Explore sales, demand, revenue, and product categories.
4. **Database Management:** Load prepared datasets into PostgreSQL.
5. **SQL Analytics:** Perform advanced business analysis using SQL.
6. **Demand Forecasting:** Train and evaluate forecasting approaches.
7. **Business Insights:** Generate rule-based insights from calculated metrics.
8. **Dashboard Development:** Present analytical results using Power BI.
9. **Pipeline Automation:** Execute the major processing stages through one Python command.

### Architecture Diagram

![RetailIQ Architecture](docs/retailiq_architecture.png)

## Machine Learning and Forecasting

The forecasting component focuses on five major product categories:

- Bed & Bath Table
- Health & Beauty
- Sports & Leisure
- Furniture & Decor
- Computers & Accessories

The project compares Random Forest predictions with a baseline forecasting approach.

Evaluation metrics include:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

The dataset has a limited historical time range, so model performance is evaluated using a chronological train-test split. The simpler baseline performed better for most categories under the selected MAE comparison.

A three-month moving-average fallback is also used when generating future forecasts for selected categories.

## PostgreSQL Analytics

The project includes SQL analysis for:

- Overall business performance
- Monthly revenue trends
- Top-performing product categories
- Customer repeat-purchase analysis
- Delivery performance
- Month-over-month revenue growth
- Category revenue contribution
- Forecast model comparison
- Future demand ranking

Advanced SQL concepts include CTEs, window functions, `LAG()`, `RANK()`, and aggregate functions.

## Power BI Dashboard

The Power BI report contains three analytical pages:

1. **Executive Overview** – Business performance and revenue analysis.
2. **Customer & Operations** – Customer and delivery-related analysis.
3. **Demand Forecasting & Model Performance** – Historical demand, forecast comparisons, and model evaluation.

## Business Insights Engine

A Python-based, rule-driven insights component generates business observations and recommendations using calculated dataset metrics and forecasting outputs.

It is a rule-based analytics component, not a generative AI model.

## Project Structure

```text
RetailIQ/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── config.py
│   ├── profile_data.py
│   ├── prepare_data.py
│   ├── load_to_postgres.py
│   ├── explore_demand.py
│   ├── forecast_demand.py
│   ├── generate_forecast.py
│   ├── visualize_forecast.py
│   ├── load_forecast_to_postgres.py
│   ├── generate_business_insights.py
│   ├── load_business_insights_to_postgres.py
│   └── run_retailiq_pipeline.py
│
├── sql/
│   ├── retailiq_analysis.sql
│   └── advanced_retailiq_analytics.sql
│
├── notebooks/
├── dashboard/
├── models/
├── outputs/
├── docs/
│
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RetailIQ
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib sqlalchemy psycopg2-binary python-dotenv
```

### 4. Configure PostgreSQL

- Install PostgreSQL.
- Create a database named `retailiq`.
- Copy `.env.example` to `.env`.
- Enter your local PostgreSQL credentials in `.env`.

Never upload your actual `.env` file.

### 5. Add the dataset

Download the Olist dataset from Kaggle and place the required CSV files inside `data/raw/`.

### 6. Run the automated pipeline

From the project root:

```bash
python src/run_retailiq_pipeline.py
```

### 7. Execute SQL analytics

Open the SQL files inside the `sql/` directory and execute the queries using pgAdmin Query Tool.

### 8. Open the Power BI report

Open the `.pbix` report in Power BI Desktop and configure the PostgreSQL connection for your environment.

## Current Project Status

- Historical dataset preparation completed.
- PostgreSQL database integration completed.
- SQL business analytics implemented.
- Demand forecasting models evaluated.
- Future demand forecasts generated.
- Forecast visualizations generated.
- Power BI dashboards developed.
- Rule-based business insights generated.
- Automated Python pipeline implemented.

## Future Enhancements

- Experiment with additional time-series forecasting models.
- Expand forecasting to more product categories.
- Improve evaluation with longer historical datasets.
- Add automated data-quality monitoring.
- Explore a more interactive business-insights interface.
- Investigate scheduled data refresh and deployment.

## Author

**Aniket Halkude**  
BE – Computer Science and Data Science Engineering  
AMC Engineering College, Bengaluru

**Career Interests:** Data Analytics, Data Science, Business Intelligence, and AI-powered analytics.

## Dataset Attribution

Dataset: Brazilian E-Commerce Public Dataset by Olist  
Source: Kaggle – https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Please review the dataset's license and attribution requirements before redistributing or reusing the data.
