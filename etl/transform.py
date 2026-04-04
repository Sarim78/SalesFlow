import pandas as pd
import os


PROCESSED_DATA_PATH = os.path.join("data", "processed", "cleaned_sales.csv")

# Transform function to clean and prepare sales data for analysis
def transform(df: pd.DataFrame) -> pd.DataFrame:
    print(f"[TRANSFORM] Starting transformation on {len(df)} records...")

    # Step 1 — Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print(f"[TRANSFORM] Columns normalized: {list(df.columns)}")

    # Step 2 — Drop duplicates and rows with critical nulls
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["transaction_id", "date", "customer_id", "total_amount"])
    after = len(df)

    print(f"[TRANSFORM] Dropped {before - after} duplicate/null rows. {after} records remaining.")

    # Step 3 — Fix data types
    df["date"] = pd.to_datetime(df["date"])
    df["transaction_id"] = df["transaction_id"].astype(int)
    df["age"] = df["age"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["price_per_unit"] = df["price_per_unit"].astype(float)
    df["total_amount"] = df["total_amount"].astype(float)

    # Standardize text fields
    df["gender"] = df["gender"].str.strip().str.title()
    df["product_category"] = df["product_category"].str.strip().str.title()
    df["customer_id"] = df["customer_id"].str.strip().str.upper()

    print("[TRANSFORM] Data types fixed.")

    # Step 4 — Engineer new features
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 50, 100],
        labels=["18-25", "26-35", "36-50", "50+"]
    ).astype(str)

    # Date parts for trend analysis
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["month_year"] = df["date"].dt.to_period("M").astype(str)  # e.g. '2023-01'

    print("[TRANSFORM] Engineered features: age_group, month, year, month_year")

    # Step 5 — Save processed data to CSV
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"[TRANSFORM] Cleaned data saved to {PROCESSED_DATA_PATH}")
    print(f"[TRANSFORM] Transformation complete. {len(df)} records ready to load.")

    return df


if __name__ == "__main__":
    from extract import extract
    raw_df = extract()
    cleaned_df = transform(raw_df)
    print(cleaned_df.head())