# day04_project.py — Personal Expense Tracker

import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.title("💳 Personal Expense Tracker")
st.markdown(
    "Upload a CSV with columns: **Date, Category, Amount, Description**"
)
st.markdown("---")

# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your expenses CSV",
    type="csv",
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])
else:
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-05",
                    "2024-01-12",
                    "2024-02-01",
                    "2024-02-14",
                    "2024-03-08",
                ]
            ),
            "Category": [
                "Food",
                "Transport",
                "Food",
                "Entertainment",
                "Bills",
            ],
            "Amount": [850, 220, 1100, 550, 2500],
            "Description": [
                "Groceries",
                "Bus pass",
                "Restaurant",
                "Cinema",
                "Electricity",
            ],
        }
    )

    st.info("No file uploaded — showing sample data.")

# -----------------------------------------------------------------------------
# Filters
# -----------------------------------------------------------------------------

st.subheader("Filters")

date_range = st.date_input(
    "Date range",
    value=(
        df["Date"].min().date(),
        df["Date"].max().date(),
    ),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date(),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered = df[
        df["Date"].dt.date.between(start_date, end_date)
    ].copy()
else:
    filtered = df.copy()
    start_date = None
    end_date = None

# Category filter
categories = st.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique()),
)

if not categories:
    categories = df["Category"].unique().tolist()

filtered = filtered[
    filtered["Category"].isin(categories)
]

# Minimum amount filter
min_amount = st.slider(
    "Minimum amount (₹)",
    min_value=0,
    max_value=int(df["Amount"].max()),
    value=0,
    step=50,
)

filtered = filtered[
    filtered["Amount"] >= min_amount
]

st.markdown("---")

# -----------------------------------------------------------------------------
# Summary Metrics
# -----------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Spent",
    f"₹{filtered['Amount'].sum():,.0f}",
)

col2.metric(
    "Transactions",
    len(filtered),
)

largest_expense = (
    f"₹{filtered['Amount'].max():,.0f}"
    if not filtered.empty
    else "N/A"
)

col3.metric(
    "Largest Expense",
    largest_expense,
)

st.markdown("---")

# -----------------------------------------------------------------------------
# Expense Table
# -----------------------------------------------------------------------------

st.subheader("Filtered Expenses")

if filtered.empty:
    st.warning("No expenses match the current filters.")
else:
    styled_df = filtered.style.map(
        lambda value: (
            "color:red"
            if isinstance(value, (int, float)) and value > 1000
            else ""
        ),
        subset=["Amount"],
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------------------------------------------------------
# Download Filtered Data
# -----------------------------------------------------------------------------

filename = (
    f"expenses_{start_date}_{end_date}.csv"
    if start_date
    else "expenses.csv"
)

st.download_button(
    label="⬇️ Download Filtered CSV",
    data=filtered.to_csv(index=False),
    file_name=filename,
    mime="text/csv",
    type="primary",
)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------

st.caption("Day 4 Project · Personal Expense Tracker")