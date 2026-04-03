-- =============================================================
-- SalesFlow — Database Schema
-- =============================================================

-- Drop table if it already exists (useful for resets)
DROP TABLE IF EXISTS sales;

-- =============================================================
-- Main sales table
-- =============================================================
CREATE TABLE sales (
    id                  SERIAL PRIMARY KEY,
    transaction_id      INTEGER NOT NULL UNIQUE,
    date                DATE NOT NULL,
    customer_id         VARCHAR(20) NOT NULL,
    gender              VARCHAR(10),
    age                 INTEGER,
    product_category    VARCHAR(50),
    quantity            INTEGER,
    price_per_unit      NUMERIC(10, 2),
    total_amount        NUMERIC(10, 2),

    -- Engineered columns (added during ETL transform)
    age_group           VARCHAR(20),         -- e.g. '18-25', '26-35', '36-50', '50+'
    month               INTEGER,             -- extracted from date
    year                INTEGER,             -- extracted from date
    month_year          VARCHAR(10),         -- e.g. '2023-01' for trend grouping

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================
-- Indexes for faster analytical queries
-- =============================================================

-- Speed up date range filters
CREATE INDEX idx_sales_date ON sales(date);

-- Speed up category grouping
CREATE INDEX idx_sales_category ON sales(product_category);

-- Speed up customer aggregations
CREATE INDEX idx_sales_customer ON sales(customer_id);

-- Speed up month/year trend queries
CREATE INDEX idx_sales_month_year ON sales(month_year);

-- Speed up gender/age segment queries
CREATE INDEX idx_sales_gender ON sales(gender);
CREATE INDEX idx_sales_age_group ON sales(age_group);