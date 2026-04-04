import pytest
import pandas as pd
from etl.transform import transform

# Fixtures
@pytest.fixture
def sample_df():
    """
    Returns a minimal valid DataFrame that mirrors the raw CSV structure.
    Used as the base input across most tests.
    """
    return pd.DataFrame({
        "Transaction ID":   [1, 2, 3, 4, 5],
        "Date":             ["2023-01-15", "2023-02-20", "2023-03-10", "2023-04-05", "2023-05-18"],
        "Customer ID":      ["cust001", "CUST002", "cust003", "CUST004", "cust005"],
        "Gender":           ["male", "female", "Male", "Female", "male"],
        "Age":              [22, 34, 45, 60, 28],
        "Product Category": ["electronics", "Beauty", "CLOTHING", "electronics", "beauty"],
        "Quantity":         [2, 1, 3, 1, 2],
        "Price per Unit":   [200, 150, 50, 300, 100],
        "Total Amount":     [400, 150, 150, 300, 200],
    })


@pytest.fixture
def df_with_nulls():
    """
    Returns a DataFrame with null values in critical columns.
    Used to test null-dropping logic.
    """
    return pd.DataFrame({
        "Transaction ID":   [1, None, 3],
        "Date":             ["2023-01-15", "2023-02-20", None],
        "Customer ID":      ["CUST001", "CUST002", None],
        "Gender":           ["Male", "Female", "Male"],
        "Age":              [25, 30, 40],
        "Product Category": ["Electronics", "Beauty", "Clothing"],
        "Quantity":         [1, 2, 1],
        "Price per Unit":   [100, 50, 200],
        "Total Amount":     [100, 100, None],
    })


@pytest.fixture
def df_with_duplicates(sample_df):
    """
    Returns a DataFrame with duplicate rows.
    Used to test deduplication logic.
    """
    return pd.concat([sample_df, sample_df.iloc[[0]]], ignore_index=True)


# Column Name Tests
class TestColumnNormalization:

    def test_columns_are_lowercase(self, sample_df):
        result = transform(sample_df)
        for col in result.columns:
            assert col == col.lower(), f"Column '{col}' is not lowercase"

    def test_columns_have_no_spaces(self, sample_df):
        result = transform(sample_df)
        for col in result.columns:
            assert " " not in col, f"Column '{col}' contains a space"

    def test_expected_columns_exist(self, sample_df):
        result = transform(sample_df)
        expected = [
            "transaction_id", "date", "customer_id", "gender",
            "age", "product_category", "quantity",
            "price_per_unit", "total_amount"
        ]
        for col in expected:
            assert col in result.columns, f"Expected column '{col}' not found"


# Data Cleaning Tests
class TestDataCleaning:

    def test_duplicates_are_removed(self, df_with_duplicates):
        result = transform(df_with_duplicates)
        assert result.duplicated().sum() == 0

    def test_null_critical_rows_are_dropped(self, df_with_nulls):
        result = transform(df_with_nulls)
        assert result["transaction_id"].isnull().sum() == 0
        assert result["date"].isnull().sum() == 0
        assert result["customer_id"].isnull().sum() == 0
        assert result["total_amount"].isnull().sum() == 0

    def test_gender_is_title_case(self, sample_df):
        result = transform(sample_df)
        for val in result["gender"].dropna():
            assert val == val.title(), f"Gender value '{val}' is not title case"

    def test_product_category_is_title_case(self, sample_df):
        result = transform(sample_df)
        for val in result["product_category"].dropna():
            assert val == val.title(), f"Category value '{val}' is not title case"

    def test_customer_id_is_uppercase(self, sample_df):
        result = transform(sample_df)
        for val in result["customer_id"].dropna():
            assert val == val.upper(), f"Customer ID '{val}' is not uppercase"


# Data Type Tests
class TestDataTypes:

    def test_date_is_datetime(self, sample_df):
        result = transform(sample_df)
        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_total_amount_is_float(self, sample_df):
        result = transform(sample_df)
        assert pd.api.types.is_float_dtype(result["total_amount"])

    def test_quantity_is_integer(self, sample_df):
        result = transform(sample_df)
        assert pd.api.types.is_integer_dtype(result["quantity"])

    def test_age_is_integer(self, sample_df):
        result = transform(sample_df)
        assert pd.api.types.is_integer_dtype(result["age"])


# Feature Engineering Tests
class TestFeatureEngineering:

    def test_age_group_column_exists(self, sample_df):
        result = transform(sample_df)
        assert "age_group" in result.columns

    def test_age_group_valid_values(self, sample_df):
        result = transform(sample_df)
        valid = {"18-25", "26-35", "36-50", "50+"}
        for val in result["age_group"].dropna():
            assert val in valid, f"Unexpected age_group value: '{val}'"

    def test_month_column_exists(self, sample_df):
        result = transform(sample_df)
        assert "month" in result.columns

    def test_year_column_exists(self, sample_df):
        result = transform(sample_df)
        assert "year" in result.columns

    def test_month_year_column_exists(self, sample_df):
        result = transform(sample_df)
        assert "month_year" in result.columns

    def test_month_year_format(self, sample_df):
        result = transform(sample_df)
        for val in result["month_year"]:
            assert len(val) == 7, f"month_year '{val}' is not in YYYY-MM format"
            assert val[4] == "-", f"month_year '{val}' missing dash separator"

    def test_month_values_in_range(self, sample_df):
        result = transform(sample_df)
        assert result["month"].between(1, 12).all()

    def test_year_values_are_positive(self, sample_df):
        result = transform(sample_df)
        assert (result["year"] > 0).all()


# Output Tests
class TestOutput:

    def test_returns_dataframe(self, sample_df):
        result = transform(sample_df)
        assert isinstance(result, pd.DataFrame)

    def test_output_not_empty(self, sample_df):
        result = transform(sample_df)
        assert len(result) > 0

    def test_processed_csv_is_saved(self, sample_df, tmp_path, monkeypatch):
        # Redirect output path to a temp directory for testing
        import etl.transform as transform_module
        monkeypatch.setattr(
            transform_module,
            "PROCESSED_DATA_PATH",
            str(tmp_path / "cleaned_sales.csv")
        )
        transform(sample_df)
        assert (tmp_path / "cleaned_sales.csv").exists()