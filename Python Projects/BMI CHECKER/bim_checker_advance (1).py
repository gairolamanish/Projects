# bmi_advanced_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import os
from datetime import datetime
from io import BytesIO
from typing import Tuple
from fpdf import FPDF

# Try import for PDF generation (optional)
try:
    
    FPDF_AVAILABLE = True
except Exception:
    FPDF_AVAILABLE = False

# -------------------------------
# Core logic functions (your logic reused/kept)
# -------------------------------

def bmi(weight: float, height: float) -> float:
    """Calculate BMI from weight (kg) and height (m)."""
    return weight / (height ** 2)

def classify_bmi(bmi_val: float, age: int) -> Tuple[str, str, str]:
    """
    Classify BMI into categories and provide health advice.
    Returns (status, advice, note)
    """
    if bmi_val < 18.5:
        status = "Underweight"
        advice = (
            "Consider a balanced increase in calories and nutrient-dense foods. "
            "Consult a professional if concerned."
        )
    elif 18.5 <= bmi_val < 25:
        status = "Normal weight"
        advice = "Great — maintain with balanced diet and regular physical activity."
    elif 25 <= bmi_val < 30:
        status = "Overweight"
        advice = (
            "Increase physical activity and reduce energy-dense / sugary foods. "
            "Small changes add up."
        )
    else:
        status = "Obese"
        advice = (
            "Consider a comprehensive plan with diet and activity changes; "
            "consult a healthcare professional for personalized guidance."
        )

    note = ""
    if age < 18:
        note = (
            "Note: BMI categories for children/teens are different (percentiles). "
            "This result uses adult thresholds."
        )

    return status, advice, note

def age_group(age: int) -> str:
    """Return age group label for given age."""
    if age < 13:
        return "Child"
    elif 13 <= age < 18:
        return "Teen"
    elif 18 <= age < 60:
        return "Adult"
    else:
        return "Senior"

# -------------------------------
# Additional health calculations
# -------------------------------

def bmr_mifflin_segar(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
    sex: 'male' or 'female'
    Returns BMR (kcal/day).
    """
    if sex.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def daily_calorie_needs(bmr: float, activity_level: str) -> float:
    """
    Multiply BMR by activity factor:
    sedentary, lightly_active, moderately_active, very_active, extra_active
    """
    multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9,
    }
    return bmr * multipliers.get(activity_level, 1.2)

def health_risk_estimate(bmi_val: float, age: int, sex: str) -> str:
    """
    A simple heuristic to estimate health risk based on BMI and age.
    This is NOT medical advice; it's for rough guidance only.
    """
    risk = "Low"
    if bmi_val >= 30:
        risk = "High"
    elif 25 <= bmi_val < 30:
        risk = "Moderate"
    else:
        risk = "Low"

    # Age factor increases risk for older users
    if age >= 60 and risk == "Moderate":
        risk = "High"
    if age >= 60 and risk == "Low" and bmi_val >= 25:
        risk = "Moderate"

    # Adjust for sex (very slight heuristic; not clinical)
    if sex.lower() == "male" and bmi_val >= 25:
        # men with overweight get slightly higher warning
        if risk == "Low":
            risk = "Moderate"

    return risk

# -------------------------------
# Persistence (history)
# -------------------------------

HISTORY_CSV = "bmi_history.csv"

def append_history(record: dict):
    """Append a record (dict) to history CSV file (creates file if not exists)."""
    df = pd.DataFrame([record])
    if os.path.exists(HISTORY_CSV):
        df.to_csv(HISTORY_CSV, mode="a", header=False, index=False)
    else:
        df.to_csv(HISTORY_CSV, index=False)

def load_history() -> pd.DataFrame:
    if os.path.exists(HISTORY_CSV):
        return pd.read_csv(HISTORY_CSV)
    return pd.DataFrame(columns=[
        "timestamp","name","age","sex","height_m","weight_kg","bmi","category","advice","note"
    ])

# -------------------------------
# Export utilities
# -------------------------------

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def record_to_pdf_bytes(record: dict) -> bytes:
    if not FPDF_AVAILABLE:
        raise RuntimeError("fpdf not installed")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_doc_option("core_fonts_encoding", "utf-8")
    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 8, "BMI Report", ln=True, align="C")
    pdf.ln(4)

    for k, v in record.items():
        pdf.multi_cell(0, 8, f"{k}: {v}")

    return pdf.output(dest="S").encode("utf-8")

# -------------------------------
# UI helpers
# -------------------------------

def plot_bmi_gauge(bmi_val: float) -> go.Figure:
    """Return a Plotly gauge for BMI value."""
    # choose color for bar
    if bmi_val < 18.5:
        bar_color = "blue"
    elif 18.5 <= bmi_val < 25:
        bar_color = "green"
    elif 25 <= bmi_val < 30:
        bar_color = "orange"
    else:
        bar_color = "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(bmi_val, 2),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BMI"},
        gauge={
            'axis': {'range': [0, 45]},
            'bar': {'color': bar_color},
            'steps': [
                {'range': [0, 18.5], 'color': 'lightblue'},
                {'range': [18.5, 25], 'color': 'lightgreen'},
                {'range': [25, 30], 'color': 'orange'},
                {'range': [30, 45], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bmi_val
            }
        }
    ))
    fig.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20))
    return fig

def plot_history(df: pd.DataFrame) -> go.Figure:
    """Line chart of BMI history over time (if available)."""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No history yet")
        return fig
    df_sorted = df.copy()
    df_sorted['timestamp'] = pd.to_datetime(df_sorted['timestamp'])
    df_sorted.sort_values('timestamp', inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sorted['timestamp'], y=df_sorted['bmi'],
                             mode='lines+markers', name='BMI'))
    fig.update_layout(title="BMI Over Time", xaxis_title="Date", yaxis_title="BMI", height=350)
    return fig

# -------------------------------
# Streamlit App Layout
# -------------------------------

st.set_page_config(page_title="Advanced BMI Dashboard", page_icon="🩺", layout="wide")

# Theme toggle (simple CSS switch)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

col_layout = st.columns([3,1])
with col_layout[1]:
    if st.button("Toggle Dark Mode"):
        toggle_theme()

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .reportview-container, .stApp { background-color: #0e1117; color: #E6EDF3; }
        .css-1d391kg { background-color: #0e1117; } /* input backgrounds */
        </style>
        """, unsafe_allow_html=True
    )

st.title("Advanced BMI Dashboard 🩺")
st.write("A more feature-rich BMI tool (educational purposes only).")

# --- Left column: Inputs ---
left, right = st.columns([1, 1.4])

with left:
    st.header("Your Info")
    name = st.text_input("Name", value="Anonymous")
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=30, step=1)
    sex = st.selectbox("Sex", ["male", "female"])
    height_unit = st.selectbox("Height unit", ["meters", "centimeters", "inches"])
    weight_unit = st.selectbox("Weight unit", ["kilograms", "pounds"])

    # Flexible height input (allow feet+inches)
    if st.checkbox("Enter height as feet + inches"):
        feet = st.number_input("Feet", min_value=0, max_value=8, value=5, step=1)
        inches = st.number_input("Inches", min_value=0, max_value=11, value=7, step=1)
        height_m = (feet * 0.3048) + (inches * 0.0254)
        st.caption(f"Converted height: {height_m:.2f} m")
    else:
        height_input = st.number_input("Height", min_value=0.0, step=0.01)
        if height_unit == "centimeters":
            height_m = height_input / 100.0
        elif height_unit == "inches":
            height_m = height_input * 0.0254
        else:
            height_m = height_input

    weight_input = st.number_input("Weight", min_value=0.0, step=0.1)
    if weight_unit == "pounds":
        weight_kg = weight_input * 0.45359237
    else:
        weight_kg = weight_input

    st.header("Activity & Goals")
    activity_level = st.selectbox("Activity level",
                                  ["sedentary", "lightly active", "moderately active", "very active", "extra active"])
    target_weight = st.number_input("Target weight (kg)", min_value=0.0, step=0.1, value=weight_kg)
    weekly_rate = st.slider("Expected weekly change (kg/week)", min_value=0.0, max_value=1.5, value=0.25, step=0.05)
    save_history = st.checkbox("Save this check to history", value=True)

    # Button to compute
    compute = st.button("Compute BMI & Plan")

with right:
    st.header("Results & Visuals")

    # Placeholder containers
    result_container = st.empty()
    gauge_container = st.empty()
    advice_container = st.empty()
    summary_container = st.empty()

# When user clicks compute
if compute:
    # Basic validation
    if height_m <= 0 or weight_kg <= 0:
        st.error("Height and weight must be positive numbers.")
    else:
        bmi_val = bmi(weight_kg, height_m)
        status, advice, note = classify_bmi(bmi_val, age)
        ag = age_group(age)
        bmr = bmr_mifflin_segar(weight_kg, height_m * 100.0, age, sex)
        daily_cal = daily_calorie_needs(bmr, activity_level)
        risk = health_risk_estimate(bmi_val, age, sex)

        # Weight goal planner
        if target_weight == weight_kg:
            weeks_needed = 0
        else:
            diff = abs(target_weight - weight_kg)
            weeks_needed = math.ceil(diff / (weekly_rate if weekly_rate > 0 else 0.0001))

        # Build record
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "name": name,
            "age": age,
            "sex": sex,
            "height_m": round(height_m, 3),
            "weight_kg": round(weight_kg, 2),
            "bmi": round(bmi_val, 2),
            "category": status,
            "advice": advice,
            "note": note,
        }

        # Save history if requested
        if save_history:
            append_history(record)
            st.success("Result saved to local history.")

        # Show summary
        with result_container:
            st.subheader("Summary")
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Age:** {age} ({ag}) | **Sex:** {sex}")
            st.markdown(f"**Height:** {height_m:.2f} m | **Weight:** {weight_kg:.1f} kg")
            st.markdown(f"**BMI:** {bmi_val:.2f}")
            if status == "Normal weight":
                st.success(f"Category: {status}")
            elif status == "Underweight":
                st.warning(f"Category: {status}")
            else:
                st.error(f"Category: {status}")

            if note:
                st.info(note)

        with gauge_container:
            fig = plot_bmi_gauge(bmi_val)
            st.plotly_chart(fig, use_container_width=True)

        with advice_container:
            st.header("Advice & Plan")
            st.markdown(f"**Health Advice:** {advice}")
            st.markdown(f"**Estimated BMR:** {bmr:.0f} kcal/day")
            st.markdown(f"**Estimated Daily Calories (with activity):** {daily_cal:.0f} kcal/day")
            st.markdown(f"**Estimated Health Risk Level:** **{risk}**")
            if weeks_needed == 0:
                st.markdown("You are already at your target weight.")
            else:
                plan_text = f"To reach {target_weight:.1f} kg from {weight_kg:.1f} kg at {weekly_rate:.2f} kg/week will take about {weeks_needed} week(s)."
                st.markdown(plan_text)

            st.caption("This is informational only; consult healthcare professionals for personalized plans.")

        # Exports
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            # CSV of single record
            df_record = pd.DataFrame([record])
            csv_bytes = df_to_csv_bytes(df_record)
            st.download_button("Download result (.csv)", data=csv_bytes, file_name=f"bmi_result_{timestamp}.csv", mime="text/csv")
        with export_col2:
            if FPDF_AVAILABLE:
                pdf_bytes = record_to_pdf_bytes(record)
                st.download_button("Download result (.pdf)", data=pdf_bytes, file_name=f"bmi_result_{timestamp}.pdf", mime="application/pdf")
            else:
                st.info("Install 'fpdf' to enable PDF export (pip install fpdf)")

# -------------------------------
# History tab / viewer & export
# -------------------------------
st.markdown("---")
st.header("History & Progress")

hist_df = load_history()
if hist_df.empty:
    st.info("No saved history yet. Use 'Save this check to history' when you compute a result.")
else:
    # Show a preview
    st.dataframe(hist_df.sort_values("timestamp", ascending=False).head(20))

    # Plot history
    fig_hist = plot_history(hist_df)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Export history
    csv_hist_bytes = df_to_csv_bytes(hist_df)
    st.download_button("Download full history (.csv)", data=csv_hist_bytes, file_name="bmi_history.csv", mime="text/csv")

    if FPDF_AVAILABLE:
        last10 = hist_df.sort_values("timestamp", ascending=False).head(10)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_doc_option("core_fonts_encoding", "utf-8")
        pdf.set_font("Helvetica", size=12)

        pdf.cell(0, 8, "BMI History (last 10)", ln=True, align="C")
        pdf.ln(4)

        for _, row in last10.iterrows():
            pdf.multi_cell(0, 7, f"{row['timestamp']} - {row['name']} - BMI: {row['bmi']} - {row['category']}")

        pdf_bytes = pdf.output(dest="S").encode("utf-8")

        st.download_button(
            "Download history (.pdf)",
            data=pdf_bytes,
            file_name="bmi_history_last10.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Install 'fpdf' to enable PDF export for history (pip install fpdf)")

st.markdown("---")
st.markdown("**Note:** This tool provides general information only and is not a substitute for professional medical advice.")
