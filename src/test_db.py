
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Load database settings
load_dotenv()

# Read connection details
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

# Create database connection
engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version(), current_database()")
        )

        version, database = result.fetchone()

        print("\nPostgreSQL connection successful!")
        print("Database:", database)
        print("Version:", version)

except Exception as error:
    print("\nDatabase connection failed!")
    print("Error:", error)

finally:
    engine.dispose()
