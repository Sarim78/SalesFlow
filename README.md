# SalesFlow

> A Python + SQL + Power BI project that builds a full ETL pipeline on raw retail sales data and surfaces revenue trends, top products, and customer segments through an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.0-150458?logo=pandas)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)

---

## Overview

SalesFlow is an end-to-end data pipeline and analytics project built on a real-world retail sales dataset. It ingests raw CSV data, cleans and transforms it using pandas, loads it into a PostgreSQL database, and surfaces business insights through a Power BI dashboard.

The project is structured around a modular **Extract → Transform → Load** architecture, with optimized SQL queries answering four core business questions.

---

## Features

- **ETL Pipeline** --> Automated ingestion, cleaning, and normalization of raw retail sales data
- **PostgreSQL Integration** --> Structured schema with indexes for fast analytical queries
- **SQL Analytics** --> Queries for top products, monthly revenue, customer lifetime value, and regional breakdowns
- **Power BI Dashboard** --> Interactive visuals for revenue trends, top categories, and customer segments

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Data Processing | pandas, NumPy |
| Database | PostgreSQL 15 |
| ORM / DB Interface | psycopg2, SQLAlchemy |
| BI Reporting | Power BI |
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
├── main.py                                # Orchestrates the full ETL pipeline
├── setup.bat                              # Automated Windows setup script
├── requirements.txt                       # Python dependencies
├── .env                                   # Database credentials (not committed)
├── .gitignore
└── README.md
```

---

## Getting Started

> **Windows users:** Just double-click `setup.bat` — it handles everything automatically. Make sure your `.env` file is configured first (see Step 3 below).

If you prefer to run manually, follow these steps:

---

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11+ | https://python.org/downloads |
| PostgreSQL | 15+ | https://www.postgresql.org/download |
| Power BI Desktop | latest | https://powerbi.microsoft.com/desktop |

Verify your installations:

```
python --version
psql --version
```

---

### Step 1 — Clone the Repository

```
git clone https://github.com/Sarim78/SalesFlow.git
cd SalesFlow
```

---

### Step 2 — Create a Virtual Environment and Install Dependencies

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 3 — Configure Environment Variables

Create a `.env` file in the root of the project folder:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=salesflow
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

> **Note:** Never commit this file to GitHub. It is already listed in `.gitignore`.

---

### Step 4 — Set Up the PostgreSQL Database

```
psql -U postgres -c "CREATE DATABASE salesflow;"
psql -U postgres -d salesflow -f sql/schema.sql
```

---

### Step 5 — Run the ETL Pipeline

```
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

### Step 6 — Connect Power BI to PostgreSQL

1. Open **Power BI Desktop**
2. Click **Get Data** → **PostgreSQL database**
3. Enter your connection details:
   - Server: `localhost`
   - Database: `salesflow`
4. Select the `sales` table and click **Load**
5. Build your visuals using the loaded data

---

## SQL Analytics

| Query | Business Question |
|-------|------------------|
| `top_products.sql` | Which product categories drive the most revenue? |
| `monthly_revenue.sql` | How has revenue trended month over month? |
| `customer_lifetime_value.sql` | What is the average spend per customer? |
| `regional_breakdown.sql` | How does sales performance vary by region/segment? |

---

## Dataset

**Source:** [Retail Sales Dataset — Kaggle](https://www.kaggle.com/)

- 1,000 transaction records
- Fields: `Transaction ID`, `Date`, `Customer ID`, `Gender`, `Age`, `Product Category`, `Quantity`, `Price per Unit`, `Total Amount`

---
