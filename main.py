import sys
import time
from etl.extract import extract
from etl.transform import transform
from etl.load import load

# Main function to run the entire ETL pipeline
def run_pipeline():
    print("=" * 55)
    print("           SalesFlow ETL Pipeline")
    print("=" * 55)

    start_time = time.time()

    # Step 1 — Extract
    print("\n[1/3] EXTRACT")
    print("-" * 55)
    try:
        raw_df = extract()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print("[ERROR] Make sure retail_sales_dataset.csv is in data/raw/")
        sys.exit(1)

    # Step 2 — Transform
    print("\n[2/3] TRANSFORM")
    print("-" * 55)
    try:
        cleaned_df = transform(raw_df)
    except Exception as e:
        print(f"[ERROR] Transform step failed: {e}")
        sys.exit(1)

    # Step 3 — Load
    print("\n[3/3] LOAD")
    print("-" * 55)
    try:
        load(cleaned_df)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Load step failed: {e}")
        sys.exit(1)

    # Done
    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 55)
    print(f"  Pipeline completed successfully in {elapsed}s")
    print("=" * 55)

# Run the pipeline when this script is executed
if __name__ == "__main__":
    run_pipeline()