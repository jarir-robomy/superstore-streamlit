# =============================================================================
# End-of-Day Project: BMI & Fitness Calculator
# Week 1, Day 3 - Streamlit Foundations · Numeric & Selection Input Widgets
# Student: OJT
# =============================================================================
# How to run:  streamlit run scripts/day03_project.py
# =============================================================================

import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Reference data (from the Day 3 handout)
# -----------------------------------------------------------------------------
ACTIVITY_LEVELS = {
    "Sedentary (desk job)":           1.2,
    "Lightly active (1–3 days/wk)":   1.375,
    "Moderately active (3–5 days)":   1.55,
    "Very active (6–7 days)":         1.725,
    "Extra active (2× training)":     1.9,
}

# -----------------------------------------------------------------------------
# Step 1 - Page title and description
# -----------------------------------------------------------------------------
st.title("💪 BMI & Fitness Calculator")
st.write(
    "An interactive health calculator that estimates your **BMI**, "
    "**daily calorie need**, and **ideal weight range** from a few simple inputs."
)
st.markdown("---")

# -----------------------------------------------------------------------------
# Step 2 - User inputs (personal details)
# -----------------------------------------------------------------------------
st.header("👤 Your Details", divider="blue")

col_a, col_b = st.columns(2)
with col_a:
    name = st.text_input("Name", value="Friend")
    age  = st.number_input("Age (years)", min_value=10, max_value=100, value=20)
    sex  = st.radio("Sex", ["Male", "Female"], horizontal=True)
with col_b:
    weight = st.slider("Weight (kg)", 30.0, 150.0, 60.0, step=0.5)
    height = st.slider("Height (cm)", 100, 220, 165, step=1)

st.write(
    f"👋 Hello **{name}**! You are **{age} years** old, **{sex}**, "
    f"**{weight} kg** in weight and **{height} cm** in height."
)

st.markdown("---")

# -----------------------------------------------------------------------------
# Step 3 - BMI Calculator
# -----------------------------------------------------------------------------
st.header("⚖️ BMI Calculator", divider="green")

height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

m1, m2 = st.columns(2)
m1.metric("Your BMI", bmi)

# Choose alert based on Table 1 of the handout
if bmi < 18.5:
    category, risk = "Underweight", "Moderate"
    m2.metric("Category", category)
    st.warning(f"🟡 **{category}** — Health risk: {risk}")
elif bmi < 25.0:
    category, risk = "Normal weight", "Low"
    m2.metric("Category", category)
    st.success(f"🟢 **{category}** — Health risk: {risk}")
elif bmi < 30.0:
    category, risk = "Overweight", "Elevated"
    m2.metric("Category", category)
    st.warning(f"🟡 **{category}** — Health risk: {risk}")
else:
    category, risk = "Obese", "High"
    m2.metric("Category", category)
    st.error(f"🔴 **{category}** — Health risk: {risk}")

st.markdown("---")

# -----------------------------------------------------------------------------
# Step 4 - Activity level and daily calorie need (Mifflin-St Jeor)
# -----------------------------------------------------------------------------
st.header("🔥 Daily Calorie Need", divider="orange")

activity_label = st.selectbox(
    "Choose your activity level",
    list(ACTIVITY_LEVELS.keys()),
)
multiplier = ACTIVITY_LEVELS[activity_label]

# Mifflin-St Jeor BMR formula
if sex == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

daily_calories = round(bmr * multiplier)

cc1, cc2, cc3 = st.columns(3)
cc1.metric("BMR (kcal)", round(bmr))
cc2.metric("Activity Multiplier", multiplier)
cc3.metric("Daily Calorie Need", f"{daily_calories} kcal")

st.markdown("---")

# -----------------------------------------------------------------------------
# Step 5 - Ideal Weight Range (Robinson Formula ± 10%)
# -----------------------------------------------------------------------------
st.header("🎯 Ideal Weight Range", divider="violet")

inches_over_5ft = (height / 2.54) - 60
if sex == "Male":
    ideal_weight = 52 + 1.9 * inches_over_5ft
else:
    ideal_weight = 49 + 1.7 * inches_over_5ft

low_weight  = round(ideal_weight * 0.90, 1)
high_weight = round(ideal_weight * 1.10, 1)

iw1, iw2 = st.columns(2)
iw1.metric("Low (kg)",  f"{low_weight} kg")
iw2.metric("High (kg)", f"{high_weight} kg")

st.caption(f"Robinson Formula · Ideal ≈ {round(ideal_weight, 1)} kg (±10% range shown)")

st.markdown("---")

# -----------------------------------------------------------------------------
# Step 6 - Full Summary (on-demand button)
# -----------------------------------------------------------------------------
st.header("📋 Full Summary", divider="red")

if st.button("Show my summary"):
    st.subheader(f"Summary for {name}")

    s1, s2, s3 = st.columns(3)
    s1.metric("BMI", bmi, delta=category, delta_color="off")
    s2.metric("Daily Calories", f"{daily_calories} kcal")
    s3.metric("Ideal Weight", f"{low_weight} – {high_weight} kg")

    st.write(
        f"At **{age} years** old and **{height} cm** tall, weighing **{weight} kg**, "
        f"you fall in the **{category}** range. To maintain your current weight at a "
        f"**{activity_label}** lifestyle, your body needs about "
        f"**{daily_calories} kcal/day**. The recommended healthy weight range for your "
        f"height is **{low_weight} kg – {high_weight} kg**."
    )

# -----------------------------------------------------------------------------
# Step 7 (Bonus) - Multiselect to compare calorie need at different activity levels
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("📊 Compare Activity Levels (Bonus)", divider="rainbow")

compare = st.multiselect(
    "Tick the activity levels you want to compare",
    options=list(ACTIVITY_LEVELS.keys()),
    default=list(ACTIVITY_LEVELS.keys()),
)
if not compare:
    compare = list(ACTIVITY_LEVELS.keys())

compare_df = pd.DataFrame({
    "Activity Level":      compare,
    "Multiplier":          [ACTIVITY_LEVELS[a] for a in compare],
    "Daily Calories (kcal)": [round(bmr * ACTIVITY_LEVELS[a]) for a in compare],
})
st.dataframe(compare_df, hide_index=True, use_container_width=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("Day 3 Project · BMI & Fitness Calculator · DBI Skill Park")
