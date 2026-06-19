"""Superstore Streamlit Project — Final Capstone Dashboard.

A complete, single-file interactive dashboard built on the Sample
Superstore dataset. This script combines every Streamlit feature from
Days 1 through 10 of the course:

    Day 1   text & display       (title, header, subheader, caption, markdown)
    Day 2   data display         (dataframe, table, metric)
    Day 3   numeric inputs       (slider)
    Day 4   selection widgets    (multiselect)
    Day 5   date + download      (date_input, pd.to_datetime, download_button)
    Day 6   layout               (sidebar, columns, tabs, expander)
    Day 7   built-in charts      (line_chart, bar_chart)
    Day 8   matplotlib + plotly  (st.pyplot, st.plotly_chart)
    Day 9   cleaning + status    (np.where, success/info/warning/error)
    Day 10  caching + forms      (@st.cache_data, st.form, st.form_submit_button)

How to run
----------
From this folder (where data/samplesuperstore.csv lives) open a terminal
and type:

    streamlit run dashboard.py

A browser tab opens at http://localhost:8501. Adjust the filters in the
sidebar and click "Apply filters" — every chart, KPI and table on the
page updates to reflect the new slice.

Required packages
-----------------
    pip install streamlit pandas numpy matplotlib plotly

"""
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# 1. Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------------------------
# 2. Cached data load + cleaning
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Read the CSV once, convert date columns, and derive helper columns.

    The @st.cache_data decorator means this function runs only on the first
    call. Every subsequent rerun (and there are many — every filter change
    triggers one) reuses the cached DataFrame, which keeps the app fast.
    """
    df = pd.read_csv("final_output/samplesuperstore.csv")

    # Convert string dates into real datetimes so date_input can filter them.
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")

    # Derived columns used by charts and alerts later in the page.
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Ship Lag"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Margin"] = (df["Profit"] / df["Sales"]).round(3)
    df["Profit Band"] = np.where(
        df["Profit"] < 0, "Loss",
        np.where(df["Profit"] < 50, "Small win", "Big win"),
    )
    return df


df = load_data()


# ---------------------------------------------------------------------------
# 3. Page header
# ---------------------------------------------------------------------------
st.title("📊 Superstore Sales Dashboard")
st.caption(
    "Source: Sample Superstore — orders from Jan 2023 to Dec 2024. "
    "Built with Streamlit."
)
st.markdown("---")


# ---------------------------------------------------------------------------
# 4. Sidebar filters (wrapped in an st.form so the page only reruns on
#    Apply rather than on every keystroke).
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Filters")
    st.caption("Adjust filters then click Apply.")

    with st.form("filters_form", clear_on_submit=False):
        regions = st.multiselect(
            "Regions",
            options=sorted(df["Region"].unique()),
            default=sorted(df["Region"].unique()),
        )
        categories = st.multiselect(
            "Categories",
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique()),
        )
        segments = st.multiselect(
            "Segments",
            options=sorted(df["Segment"].unique()),
            default=sorted(df["Segment"].unique()),
        )
        ship_modes = st.multiselect(
            "Ship Modes",
            options=sorted(df["Ship Mode"].unique()),
            default=sorted(df["Ship Mode"].unique()),
        )
        date_range = st.date_input(
            "Order date range",
            value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
            min_value=df["Order Date"].min().date(),
            max_value=df["Order Date"].max().date(),
        )
        discount_range = st.slider(
            "Discount range",
            min_value=0.0,
            max_value=0.8,
            value=(0.0, 0.8),
            step=0.05,
        )
        min_sales = st.slider(
            "Min sales per order line ($)",
            min_value=0,
            max_value=10000,
            value=0,
            step=100,
        )

        submitted = st.form_submit_button(
            "Apply filters",
            type="primary",
            use_container_width=True,
        )

    st.caption("Built with Streamlit — Day 10 capstone.")


# ---------------------------------------------------------------------------
# 5. Apply filters to the cached DataFrame
# ---------------------------------------------------------------------------
# Date range can come back as a tuple of one or two dates depending on whether
# the user has finished picking both ends. Guard against the partial case.
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = df["Order Date"].min().date()
    end_date = df["Order Date"].max().date()

# Empty multiselects mean "no constraint" rather than "no rows".
def _safe(values, column):
    """Return the picked values or the column's full set when empty."""
    return values if values else df[column].unique().tolist()


mask = (
    df["Region"].isin(_safe(regions, "Region"))
    & df["Category"].isin(_safe(categories, "Category"))
    & df["Segment"].isin(_safe(segments, "Segment"))
    & df["Ship Mode"].isin(_safe(ship_modes, "Ship Mode"))
    & df["Order Date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))
    & df["Discount"].between(discount_range[0], discount_range[1])
    & (df["Sales"] >= min_sales)
)
filtered = df[mask].copy()

# Empty-state: stop early if the user filtered too aggressively.
if filtered.empty:
    st.warning(
        "No orders match the current filters. Try widening the date range "
        "or adding more categories from the sidebar."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 6. KPI cards + overall status banner
# ---------------------------------------------------------------------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
n_orders = filtered["Order ID"].nunique()
avg_disc = filtered["Discount"].mean()
overall_margin = total_profit / total_sales if total_sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric(
    "Total Profit",
    f"${total_profit:,.0f}",
    delta=f"{overall_margin:.1%} margin",
    delta_color="normal" if total_profit >= 0 else "inverse",
)
c3.metric("Orders", f"{n_orders:,}")
c4.metric("Avg Discount", f"{avg_disc:.1%}")

if total_profit > 0:
    st.success(
        f"Overall profit on the filtered slice is positive: "
        f"${total_profit:,.0f} ({overall_margin:.1%} margin)."
    )
else:
    st.error(
        f"Overall profit on the filtered slice is NEGATIVE: "
        f"${total_profit:,.0f}. Loosen the discount range or drop "
        f"loss-making sub-categories."
    )

st.markdown("---")


# ---------------------------------------------------------------------------
# 7. Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "By Category", "Customers", "Quality alerts"]
)

# --- Tab 1: Overview ----------------------------------------------------
with tab1:
    left, right = st.columns([2, 1])

    with left:
        st.subheader("Monthly Sales and Profit")
        month_idx = filtered["Order Date"].dt.to_period("M")
        monthly = (
            filtered.groupby(month_idx)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .round(2)
        )
        monthly.index = monthly.index.to_timestamp()
        st.line_chart(monthly, height=320)
        st.caption("Sales and Profit aggregated by calendar month.")

    with right:
        st.subheader("Sales by Region")
        sales_region = (
            filtered.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
        )
        st.bar_chart(sales_region, height=320)
        st.caption("Sum of Sales for each region.")

    st.subheader("Sales by Segment")
    sales_segment = (
        filtered.groupby("Segment")[["Sales", "Profit"]].sum().round(2)
    )
    st.bar_chart(sales_segment, height=260)

# --- Tab 2: By Category --------------------------------------------------
with tab2:
    st.subheader("Top 15 Sub-Categories by Sales")
    top_sub = (
        filtered.groupby("Sub-Category")["Sales"]
        .sum()
        .nlargest(15)
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_sub.index, top_sub.values, color="#3b82f6")
    ax.set_xlabel("Sales ($)")
    ax.set_title("Top 15 Sub-Categories")
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Category → Sub-Category treemap")
    treemap_data = (
        filtered.groupby(["Category", "Sub-Category"])["Sales"]
        .sum()
        .round(2)
        .reset_index()
    )
    fig2 = px.treemap(
        treemap_data,
        path=["Category", "Sub-Category"],
        values="Sales",
        color="Sales",
        color_continuous_scale="Blues",
    )
    fig2.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=420)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Sub-Category leaderboard")
    sub_summary = (
        filtered.groupby("Sub-Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Avg_Discount=("Discount", "mean"),
        )
        .round(2)
        .sort_values("Sales", ascending=False)
    )
    st.dataframe(sub_summary, use_container_width=True)

# --- Tab 3: Customers ----------------------------------------------------
with tab3:
    st.subheader("Top 10 Customers by Sales")
    top_customers = (
        filtered.groupby("Customer Name")["Sales"]
        .sum()
        .nlargest(10)
        .round(2)
        .reset_index()
    )
    st.table(top_customers)

    st.subheader("Underlying filtered rows")
    st.dataframe(
        filtered[
            [
                "Order Date",
                "Customer Name",
                "Segment",
                "Region",
                "Category",
                "Sub-Category",
                "Sales",
                "Quantity",
                "Discount",
                "Profit",
            ]
        ].head(200),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        f"Showing first 200 of {filtered.shape[0]:,} filtered rows. "
        f"Click any column header to sort."
    )

# --- Tab 4: Quality alerts ----------------------------------------------
with tab4:
    st.subheader("Loss-making Sub-Categories")
    sub_profit = (
        filtered.groupby("Sub-Category")["Profit"].sum().round(2)
    )
    losers = sub_profit[sub_profit < 0].sort_values()

    if losers.empty:
        st.success(
            "All Sub-Categories are profitable under the current filters."
        )
    else:
        st.warning(
            f"{len(losers)} Sub-Categories show a negative total profit:"
        )
        for sub, val in losers.items():
            st.error(f"{sub}: ${val:,.2f} loss")

    st.subheader("Heavy-discount diagnosis")
    high_disc = filtered[filtered["Discount"] >= 0.3]
    if high_disc.empty:
        st.info(
            "No orders with discount ≥ 30% in the current slice — nothing "
            "to diagnose here."
        )
    else:
        avg_margin = (high_disc["Profit"] / high_disc["Sales"]).mean()
        share = len(high_disc) / len(filtered)
        st.write(
            f"{len(high_disc):,} orders have discount ≥ 30% "
            f"({share:.1%} of the filtered slice)."
        )
        if avg_margin < 0:
            st.error(
                f"Their average margin is {avg_margin:.1%} — heavy "
                f"discounting is destroying profitability."
            )
        elif avg_margin < 0.05:
            st.warning(
                f"Their average margin is only {avg_margin:.1%} — "
                f"discounts are eroding profitability."
            )
        else:
            st.success(
                f"Their average margin is {avg_margin:.1%} — discounts "
                f"are not hurting profitability."
            )

    st.subheader("Shipping lag distribution")
    fig3, ax3 = plt.subplots(figsize=(8, 3))
    ax3.hist(
        filtered["Ship Lag"].dropna(),
        bins=range(0, int(filtered["Ship Lag"].max()) + 2),
        color="#10b981",
        edgecolor="white",
    )
    ax3.set_xlabel("Days between order and ship")
    ax3.set_ylabel("Number of orders")
    ax3.axvline(
        filtered["Ship Lag"].mean(),
        color="red",
        linestyle="--",
        label=f"mean = {filtered['Ship Lag'].mean():.1f}",
    )
    ax3.legend()
    plt.tight_layout()
    st.pyplot(fig3)


# ---------------------------------------------------------------------------
# 8. Footer: download button + explainer
# ---------------------------------------------------------------------------
st.markdown("---")

today_str = date.today().strftime("%Y-%m-%d")
download_cols = st.columns([1, 1, 2])
download_cols[0].download_button(
    "Download filtered slice (CSV)",
    filtered.to_csv(index=False),
    file_name=f"superstore_filtered_{today_str}.csv",
    mime="text/csv",
    type="primary",
    use_container_width=True,
)
download_cols[1].download_button(
    "Download Sub-Category leaderboard",
    sub_summary.to_csv(),
    file_name=f"sub_category_leaderboard_{today_str}.csv",
    mime="text/csv",
    use_container_width=True,
)

with st.expander("How this app works"):
    st.markdown(
        "**Dataset.** Sample Superstore — one row per order line. Sales, "
        "Profit, Quantity, Discount across 17 Sub-Categories, 4 Regions, "
        "3 Segments, 4 Ship Modes, two years of orders.\n\n"
        "**Filters.** All filters live in the sidebar inside an `st.form` — "
        "the page only re-renders when you click **Apply**. This keeps "
        "the experience fast even though every interaction triggers a "
        "full Streamlit rerun.\n\n"
        "**KPIs.** Four metric cards summarise the filtered slice: Total "
        "Sales, Total Profit (with margin delta), distinct Orders, and "
        "Average Discount.\n\n"
        "**Tabs.**\n"
        "- *Overview* — monthly trend lines, per-Region totals, "
        "Sales+Profit by Segment.\n"
        "- *By Category* — horizontal bar of the top 15 Sub-Categories, "
        "a Plotly treemap of Category → Sub-Category, and a sortable "
        "leaderboard.\n"
        "- *Customers* — top 10 customers and the underlying rows.\n"
        "- *Quality alerts* — loss-making Sub-Categories, a heavy-"
        "discount margin diagnosis, and a shipping-lag histogram.\n\n"
        "**Caching.** The `load_data()` function is decorated with "
        "`@st.cache_data`, so the 10,194-row CSV is read and cleaned "
        "once and reused across every interaction.\n\n"
        "Built across 10 days of the Superstore Streamlit course."
    )

st.caption(f"Generated {today_str} • Built with Streamlit • Day 10 capstone")