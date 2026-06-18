# day06_project.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px

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


    monthly = (filtered 
                .set_index("Order Date") 
                .resample("ME")["Sales"].sum()) 
    st.subheader("Monthly Sales Trend") 
    st.line_chart(monthly)



    top10 = filtered.groupby("sub_category")["Sales"].sum().nlargest(10).sort_values() 
    fig, ax = plt.subplots(figsize=(7, 4)) 
    bars = ax.barh(top10.index, top10.values, color="#3B82F6") 
    ax.bar_label(bars, fmt="$%.0f", padding=4, fontsize=8) 
    ax.set_xlabel("Total Sales") 
    ax.set_title("Top 10 Sub-Categories by Sales") 
    plt.tight_layout() 
    st.pyplot(fig) 
    plt.close(fig) 





# --------------------------------------------------
# Category Tab
# --------------------------------------------------
with tab2:
    
    cat_sales =filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False) 
    st.subheader("Sales by Category") 
    st.bar_chart(cat_sales) 


    fig = px.scatter(filtered, x="Sales", y="Profit", 
        color="Category", size="Quantity", 
        hover_data=["sub_category"], 
        title="Sales vs Profit by Category") 
    st.plotly_chart(fig, use_container_width=True) 


    monthly_yr = ( 
        filtered .groupby([filtered.order_date.dt.to_period("M").astype(str), "order_year"])["Sales"] .sum().reset_index().rename(columns={"order_date": "Month"})) 
        fig = px.line(monthly_yr, x="Month", y="Sales", color="order_year", title="Monthly Sales by Year") 
        st.plotly_chart(fig, use_container_width=True)






# --------------------------------------------------
# Region Tab
# --------------------------------------------------
with tab3:
    st.info("Charts arrive on Day 7.")








