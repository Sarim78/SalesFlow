import pandas as pd
import os

# Define the path to the raw data CSV file
RAW_DATA_PATH = os.path.join("data", "raw", "retail_sales_dataset.csv")

# Extract function to load raw sales data from CSV file
def extract(filepath: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Extract raw sales data from CSV file into a pandas DataFrame.
 
    Args:
        filepath: Path to the raw CSV file.
 
    Returns:
        pd.DataFrame: Raw, unmodified sales data.
 
    Raises:
        FileNotFoundError: If the CSV file does not exist at the given path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[EXTRACT] File not found: {filepath}")
 
    print(f"[EXTRACT] Loading data from {filepath}...")
 
    df = pd.read_csv(filepath)
 
    print(f"[EXTRACT] Loaded {len(df)} records with {len(df.columns)} columns.")
    print(f"[EXTRACT] Columns: {list(df.columns)}")
 
    return df
 
 
if __name__ == "__main__":
    df = extract()
    print(df.head())