# SalesFlow

> A Python + SQL + Streamlit project that builds a full ETL pipeline on raw retail sales data and surfaces revenue trends, top products, and customer segments through an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.0-150458?logo=pandas)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)

---

## Overview

SalesFlow is an end-to-end data pipeline and analytics project built on a real-world retail sales dataset. It ingests raw CSV data, cleans and transforms it using pandas, loads it into a PostgreSQL database, and surfaces business insights through both a live Streamlit dashboard and a Power BI report.

The project is structured around a modular **Extract → Transform → Load** architecture, with optimized SQL queries answering four core business questions and an interactive frontend for data exploration.

---

## Features

- **ETL Pipeline** --> Automated ingestion, cleaning, and normalization of raw retail sales data
- **PostgreSQL Integration** --> Structured schema with indexes for fast analytical queries
- **SQL Analytics** --> Queries for top products, monthly revenue, customer lifetime value, and regional breakdowns
- **Streamlit Dashboard** --> Live interactive web app with filters for date range, product category, and customer segment
- **Power BI Report** --> `.pbix` file for enterprise-style reporting and stakeholder presentations
- **Unit Tested** --> Core transformation logic covered with `pytest`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Data Processing | pandas, NumPy |
| Database | PostgreSQL 15 |
| ORM / DB Interface | psycopg2, SQLAlchemy |
| Dashboard | Streamlit |
| BI Reporting | Power BI |
| Testing | pytest |
| Environment | python-dotenv |

---

## Project Structure

```
salesflow/
│
├── data/
│   ├── raw/
│   │   └── retail_sales_dataset.csv       # Original untouched dataset
│   └── processed/
│       └── cleaned_sales.csv              # Output after ETL transformations
│
├── etl/
│   ├── extract.py                         # Load raw CSV into pandas DataFrame
│   ├── transform.py                       # Clean nulls, fix types, engineer features
│   └── load.py                            # Load transformed data into PostgreSQL
│
├── sql/
│   ├── schema.sql                         # CREATE TABLE statements and indexes
│   ├── top_products.sql                   # Top categories by total revenue
│   ├── monthly_revenue.sql                # Month-over-month revenue trends
│   ├── customer_lifetime_value.sql        # CLV aggregation per customer
│   └── regional_breakdown.sql            # Sales breakdown by region/segment
│
├── dashboard/
│   └── app.py                             # Streamlit interactive dashboard
│
├── tests/
│   └── test_transform.py                  # Unit tests for ETL transform logic
│
├── main.py                                # Orchestrates the full ETL pipeline
├── requirements.txt                       # Python dependencies
├── .env                                   # Database credentials (not committed)
├── .gitignore
└── README.md
```

---

## Getting Started

Follow these steps in order to get SalesFlow running on your local machine.

---

### Step 1 — Install Prerequisites

Make sure you have the following installed before anything else:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11+ | https://python.org/downloads |
| PostgreSQL | 15+ | https://www.postgresql.org/download |
| pip | latest | comes with Python |

To verify your installations, run:

```bash
python --version      # should output Python 3.11.x or higher
psql --version        # should output psql 15.x or higher
pip --version         # should output pip 23.x or higher
```

---

### Step 2 — Clone the Repository

```bash
git clone https://github.com/Sarim78/salesflow.git
cd salesflow
```

---

### Step 3 — Create a Virtual Environment (Recommended)

This keeps your project dependencies isolated from your system Python.

```bash
# Create the virtual environment
python -m venv venv

# Activate it — Mac/Linux
source venv/bin/activate

# Activate it — Windows
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal line when it's active.

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including pandas, psycopg2, SQLAlchemy, and Streamlit.

---

### Step 5 — Set Up the PostgreSQL Database

Open your PostgreSQL shell (psql) and create a new database for the project:

```sql
CREATE DATABASE salesflow;
```

Then run the schema file to create the required tables:

```bash
psql -U your_username -d salesflow -f sql/schema.sql
```

---

### Step 6 — Configure Environment Variables

Create a `.env` file in the root of the project directory. This file stores your database credentials and is never committed to GitHub.

```bash
# Create the file
touch .env        # Mac/Linux
type nul > .env   # Windows
```

Open `.env` and add the following — replace the values with your actual PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=salesflow
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

> **Note:** Make sure `.env` is listed in your `.gitignore` so your credentials are never pushed to GitHub.

---

### Step 7 — Run the ETL Pipeline

This will extract the raw CSV, clean and transform the data, and load it into your PostgreSQL database.

```bash
python main.py
```

Expected output:

```
[EXTRACT] Loading raw data from data/raw/retail_sales_dataset.csv...
[TRANSFORM] Cleaning and engineering features...
[LOAD] Writing 1000 records to PostgreSQL...
[DONE] Pipeline completed successfully.
```

---

### Step 8 — Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

Streamlit will automatically open the dashboard in your browser at:

```
http://localhost:8501
```

---

### Step 9 — Open in Power BI (Optional)

1. Download and install Power BI Desktop (free)
   https://powerbi.microsoft.com/desktop

2. Open Power BI Desktop

3. Click Get Data → PostgreSQL database

4. Enter your connection details:
   - Server: localhost
   - Database: salesflow

5. Select the sales table and click Load

6. Open the included salesflow.pbix file
   (File → Open → salesflow.pbix)

---

## SQL Analytics

The `sql/` directory contains four optimized queries that answer core business questions:

| Query | Business Question |
|-------|------------------|
| `top_products.sql` | Which product categories drive the most revenue? |
| `monthly_revenue.sql` | How has revenue trended month over month? |
| `customer_lifetime_value.sql` | What is the average spend per customer? |
| `regional_breakdown.sql` | How does sales performance vary by region/segment? |

---

## Dashboard Preview

The Streamlit dashboard includes:

- **Revenue Over Time** --> Line chart with monthly granularity
- **Top Categories** --> Bar chart ranked by total sales
- **Customer Segments** --> Breakdown by age group and gender
- **KPI Cards** --> Total revenue, average order value, total transactions
- **Filters** --> Date range, product category, customer segment

---

## Dataset

**Source:** [Retail Sales Dataset — Kaggle](https://www.kaggle.com/)

- 1,000 transaction records
- Fields: `Transaction ID`, `Date`, `Customer ID`, `Gender`, `Age`, `Product Category`, `Quantity`, `Price per Unit`, `Total Amount`

---

## Running Tests

```bash
pytest tests/
```

---
