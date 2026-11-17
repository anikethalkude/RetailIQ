
from pathlib import Path
import pandas as pd
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# ==========================================
# RETAILIQ - SAVE BUSINESS INSIGHTS TO POSTGRESQL
# ==========================================

ROOT = Path(__file__).resolve().parents[1]

INSIGHT_FILE = ROOT / "outputs" / "business_insights.txt"

# Load database credentials securely
load_dotenv(ROOT / ".env")

required_settings = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD"
]

for setting in required_settings:
    if not os.getenv(setting):
        raise ValueError(
            f"Missing {setting} in your .env file."
        )

# Check insight file
if not INSIGHT_FILE.exists():
    raise FileNotFoundError(
        f"Insight file not found: {INSIGHT_FILE}"
    )

# Read generated insights
lines = INSIGHT_FILE.read_text(
    encoding="utf-8"
).splitlines()

records = []
current_section = "General"

for line in lines:

    line = line.strip()

    if not line or set(line) == {"="}:
        continue

    # Identify report sections
    if line[:1].isdigit() and ". " in line:
        current_section = line.split(". ", 1)[1]
        continue

    if line.startswith("RETAILIQ"):
        continue

    if line.startswith("END OF"):
        continue

    records.append({
        "section": current_section,
        "insight": line.lstrip("- ").strip()
    })

if not records:
    raise ValueError(
        "No business insights found in the report."
    )

df = pd.DataFrame(records)

# Add generation timestamp
df["generated_at"] = pd.Timestamp.now(tz="UTC")

# Connect to PostgreSQL
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(
    database_url,
    pool_pre_ping=True
)

print("\nRETAILIQ BUSINESS INSIGHTS UPLOAD")
print("=" * 50)

try:
    # Replace only the business_insights table
    df.to_sql(
        name="business_insights",
        con=engine,
        schema="public",
        if_exists="replace",
        index=False
    )

    # Verify uploaded records
    with engine.connect() as connection:
        count = connection.execute(
            text(
                "SELECT COUNT(*) FROM public.business_insights"
            )
        ).scalar_one()

    print(f"Insights uploaded: {count}")
    print("PostgreSQL table: public.business_insights")
    print("UPLOAD COMPLETED SUCCESSFULLY!")

except Exception as error:
    print("UPLOAD FAILED!")
    print("Error:", error)
    raise

finally:
    engine.dispose()
