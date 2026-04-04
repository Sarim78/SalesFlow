import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "salesflow")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Function to create a SQLAlchemy engine for PostgreSQL connection
def get_engine():
    if not DB_USER or not DB_PASSWORD:
        raise ValueError(
            "[LOAD] Missing database credentials. "
            "Make sure DB_USER and DB_PASSWORD are set in your .env file."
        )

    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_string)
    return engine


# Load function to write cleaned data into PostgreSQL database
def load(df: pd.DataFrame, table_name: str = "sales") -> None:
    print(f"[LOAD] Connecting to PostgreSQL database '{DB_NAME}' on {DB_HOST}:{DB_PORT}...")

    engine = get_engine()

    # Verify connection before attempting load
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("[LOAD] Connection successful.")

    print(f"[LOAD] Writing {len(df)} records to table '{table_name}'...")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",   # drop and recreate table on each run
        index=False,
        chunksize=500,          # write in batches of 500 rows
        method="multi"          # faster bulk insert
    )

    print(f"[LOAD] Successfully loaded {len(df)} records into '{table_name}'.")
    print("[LOAD] Load step complete.")

# Main block to run load function independently
if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw_df = extract()
    cleaned_df = transform(raw_df)
    load(cleaned_df)