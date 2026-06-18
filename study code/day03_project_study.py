# =============================================================================
# Superstore Data Analysis - Week 1, Day 3
# Phase 1: Streamlit Foundations - Numeric & Selection Input Widgets
# Student: OJT
# Practice Tasks T1 to T10
# =============================================================================
# How to run:  streamlit run scripts/ojt_w1d3_code.py
# =============================================================================

import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Shared demo DataFrame used across tasks T3, T4, T6, T7, T8, T9, T10
# -----------------------------------------------------------------------------
df_master = pd.DataFrame({
    "Name":  ["Aisha", "Bob", "Clara", "Dev", "Eva",
              "Finn", "Grace", "Hiro", "Ines", "Jay"],
    "Score": [88, 42, 76, 91, 35, 67, 85, 49, 78, 95],
})

st.title("🎛️ Day 3 - Practice Tasks (T1 to T10)")
st.caption("Numeric & Selection Input Widgets")

# -----------------------------------------------------------------------------
# T1 - Single-value slider
# -----------------------------------------------------------------------------
st.header("T1 — Single-value slider", divider="blue")
val = st.slider("Choose a %", 0, 100, 50, step=5)
st.write("You chose:", val)

# -----------------------------------------------------------------------------
# T2 - Two-handle range slider
# -----------------------------------------------------------------------------
st.header("T2 — Two-handle range slider", divider="blue")
lo, hi = st.slider("Price range", 0, 1000, (100, 500))
st.write(f"Range: {lo} to {hi}")

# -----------------------------------------------------------------------------
# T3 - Number input with limits
# -----------------------------------------------------------------------------
st.header("T3 — Number input with limits", divider="blue")
n = st.number_input("Top N", min_value=1, max_value=20, value=5)
st.dataframe(df_master.head(int(n)), hide_index=True)

# -----------------------------------------------------------------------------
# T4 - Text search
# -----------------------------------------------------------------------------
st.header("T4 — Text search", divider="blue")
search = st.text_input("Search name")
if search:
    st.dataframe(
        df_master[df_master["Name"].str.contains(search, case=False)],
        hide_index=True,
    )

# -----------------------------------------------------------------------------
# T5 - Selectbox
# -----------------------------------------------------------------------------
st.header("T5 — Selectbox", divider="blue")
cat = st.selectbox("Category", ["Electronics", "Clothing", "Groceries"])
st.write("Selected:", cat)

# -----------------------------------------------------------------------------
# T6 - Multiselect with default + guard
# -----------------------------------------------------------------------------
st.header("T6 — Multiselect with default", divider="blue")
opts = ["Electronics", "Clothing", "Groceries"]
sel = st.multiselect("Pick categories", opts, default=opts)
if not sel:
    sel = opts
st.write("Active filters:", sel)

# -----------------------------------------------------------------------------
# T7 - Radio buttons (horizontal)
# -----------------------------------------------------------------------------
st.header("T7 — Radio buttons", divider="blue")
sort_col = st.radio("Sort by", ["Name", "Score"], horizontal=True)
st.dataframe(df_master.sort_values(sort_col), hide_index=True)

# -----------------------------------------------------------------------------
# T8 - Checkbox filter
# -----------------------------------------------------------------------------
st.header("T8 — Checkbox filter", divider="blue")
df_t8 = df_master.copy()
show_pass = st.checkbox("Show only passes (>= 50)")
if show_pass:
    df_t8 = df_t8[df_t8["Score"] >= 50]
st.dataframe(df_t8, hide_index=True)

# -----------------------------------------------------------------------------
# T9 - Toggle chart type
# -----------------------------------------------------------------------------
st.header("T9 — Toggle chart type", divider="blue")
use_bar = st.toggle("Bar chart", value=True)
series = df_master.set_index("Name")["Score"]
if use_bar:
    st.bar_chart(series)
else:
    st.line_chart(series)

# -----------------------------------------------------------------------------
# T10 - On-demand button
# -----------------------------------------------------------------------------
st.header("T10 — On-demand button", divider="blue")
if st.button("Show stats"):
    st.write(df_master.describe())

st.markdown("---")
st.caption("Day 3 · Practice Tasks · DBI Skill Park")
