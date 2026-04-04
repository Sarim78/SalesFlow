import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Page Config
st.set_page_config(
    page_title="SalesFlow Dashboard",
    page_icon="📊",
    layout="wide"
)

# Database Connection
@st.cache_resource
def get_engine():
    DB_HOST     = os.getenv("DB_HOST", "localhost")
    DB_PORT     = os.getenv("DB_PORT", "5432")
    DB_NAME     = os.getenv("DB_NAME", "salesflow")
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


@st.cache_data
def load_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM sales", con=engine)
    df["date"] = pd.to_datetime(df["date"])
    return df


# Load Data
try:
    df = load_data()
except Exception as e:
    st.error(f"Could not connect to database. Make sure PostgreSQL is running and your .env is configured.\n\n{e}")
    st.stop()

# Sidebar Filters
st.sidebar.title("Filters")

# Date range filter
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Product category filter
categories = ["All"] + sorted(df["product_category"].unique().tolist())
selected_category = st.sidebar.selectbox("Product Category", categories)

# Gender filter
genders = ["All"] + sorted(df["gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)

# Age group filter
age_groups = ["All"] + sorted(df["age_group"].unique().tolist())
selected_age_group = st.sidebar.selectbox("Age Group", age_groups)

# Apply Filters
filtered_df = df[
    (df["date"] >= pd.Timestamp(start_date)) &
    (df["date"] <= pd.Timestamp(end_date))
]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["product_category"] == selected_category]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

if selected_age_group != "All":
    filtered_df = filtered_df[filtered_df["age_group"] == selected_age_group]

# Header
st.title("📊 SalesFlow Dashboard")
st.markdown("Retail sales analytics — revenue trends, top products, and customer segments.")
st.divider()

# KPI Cards
total_revenue       = filtered_df["total_amount"].sum()
total_transactions  = len(filtered_df)
avg_order_value     = filtered_df["total_amount"].mean()
total_units         = filtered_df["quantity"].sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Revenue",        f"${total_revenue:,.2f}")
kpi2.metric("Total Transactions",   f"{total_transactions:,}")
kpi3.metric("Avg Order Value",      f"${avg_order_value:,.2f}")
kpi4.metric("Total Units Sold",     f"{total_units:,}")

st.divider()

# Row 1 — Revenue Over Time + Top Categories
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Revenue Over Time")
    monthly = (
        filtered_df.groupby("month_year")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"month_year": "Month", "total_amount": "Revenue"})
        .sort_values("Month")
    )
    fig_line = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        labels={"Revenue": "Total Revenue ($)"},
    )
    fig_line.update_traces(line_color="#4C9BE8", marker_color="#4C9BE8")
    fig_line.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Revenue by Category")
    category_revenue = (
        filtered_df.groupby("product_category")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"product_category": "Category", "total_amount": "Revenue"})
        .sort_values("Revenue", ascending=True)
    )
    fig_bar = px.bar(
        category_revenue,
        x="Revenue",
        y="Category",
        orientation="h",
        labels={"Revenue": "Total Revenue ($)"},
        color="Revenue",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Row 2 — Gender Breakdown + Age Group Breakdown
col3, col4 = st.columns(2)

with col3:
    st.subheader("Revenue by Gender")
    gender_revenue = (
        filtered_df.groupby("gender")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"gender": "Gender", "total_amount": "Revenue"})
    )
    fig_pie = px.pie(
        gender_revenue,
        names="Gender",
        values="Revenue",
        color_discrete_sequence=["#4C9BE8", "#E87B4C"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("Revenue by Age Group")
    age_revenue = (
        filtered_df.groupby("age_group")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"age_group": "Age Group", "total_amount": "Revenue"})
        .sort_values("Age Group")
    )
    fig_age = px.bar(
        age_revenue,
        x="Age Group",
        y="Revenue",
        labels={"Revenue": "Total Revenue ($)"},
        color="Revenue",
        color_continuous_scale="Blues"
    )
    fig_age.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_age, use_container_width=True)

st.divider()

# Row 3 — Top Customers by Lifetime Value
st.subheader("Top 10 Customers by Lifetime Value")
clv = (
    filtered_df.groupby("customer_id")
    .agg(
        Total_Spent    =("total_amount", "sum"),
        Transactions   =("transaction_id", "count"),
        Avg_Order      =("total_amount", "mean")
    )
    .reset_index()
    .rename(columns={"customer_id": "Customer ID"})
    .sort_values("Total_Spent", ascending=False)
    .head(10)
)
clv["Total_Spent"] = clv["Total_Spent"].map("${:,.2f}".format)
clv["Avg_Order"]   = clv["Avg_Order"].map("${:,.2f}".format)
st.dataframe(clv, use_container_width=True, hide_index=True)

st.divider()

# Footer
st.caption("SalesFlow · Built with Python, PostgreSQL & Streamlit · github.com/Sarim78")