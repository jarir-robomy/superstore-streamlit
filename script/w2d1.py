# day06_project.py

import streamlit as st
import pandas as pd


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\jarir\Desktop\OJT BCA\project 4.1\data\superstore_clean.csv",
        parse_dates=["Order Date", "Ship Date"]
    )


df = load_data()


# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    years = st.multiselect(
        "Year",
        options=sorted(df["Order Year"].unique()),
        default=sorted(df["Order Year"].unique())
    )


# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered = df[
    (df["Region"].isin(regions))
    & (df["Order Year"].isin(years))
]


# --------------------------------------------------
# Dashboard Title
# --------------------------------------------------
st.title("📊 Superstore Sales Dashboard")


# --------------------------------------------------
# KPI Section
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${filtered['Sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${filtered['Profit'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average Discount",
        f"{filtered['Discount'].mean() * 100:.1f}%"
    )


# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["Overview", "By Category", "By Region"]
)


# --------------------------------------------------
# Overview Tab
# --------------------------------------------------
with tab1:
    st.subheader("Filtered Data Sample")

    st.dataframe(
        filtered.head(20),
        use_container_width=True
    )


# --------------------------------------------------
# Category Tab
# --------------------------------------------------
with tab2:
    st.info("Charts arrive on Day 7.")


# --------------------------------------------------
# Region Tab
# --------------------------------------------------
with tab3:
    st.info("Charts arrive on Day 7.")