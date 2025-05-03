import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Pointer fix for dropdowns
st.markdown("""
    <style>
    .stSelectbox > div {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", [
    "Concrete Strength Calculator", 
    "Soil Classification", 
    "Specific Gravity of Cement"
])

# ---------------- Concrete Strength Calculator ----------------
if option == "Concrete Strength Calculator":
    st.header("Concrete Strength from CTM Reading")
    st.markdown("**Formula:** Strength (MPa) = (CTM Reading in Tons × 1000 × 9.81) / Area in mm²")

    area = st.number_input("Enter Area (mm²)", value=1500.0)
    ctm = st.number_input("Enter CTM Reading (Tonnes)", value=10.0)

    if st.button("Calculate Strength"):
        force_n = ctm * 1000 * 9.81  # Convert ton to N
        strength = force_n / area  # MPa = N/mm²
        st.success(f"Compressive Strength = {strength:.2f} MPa")

# ---------------- Soil Classification ----------------
elif option == "Soil Classification":
    st.header("Soil Classification Based on Index Properties")

    soil_data = {
        "Liquid Limit": [30, 60, 45, 40, 50, 35],
        "Plastic Limit": [20, 25, 30, 28, 33, 24],
        "Soil Type": ["CL", "CH", "CL", "CL", "CH", "CL"]
    }

    df = pd.DataFrame(soil_data)
    X = df[["Liquid Limit", "Plastic Limit"]]
    y = df["Soil Type"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    clf = DecisionTreeClassifier()
    clf.fit(X, y_encoded)

    def get_full_form(code):
        mapping = {
            "CL": "Clay with Low Plasticity",
            "CH": "Clay with High Plasticity",
            "ML": "Silt with Low Plasticity",
            "MH": "Silt with High Plasticity",
            "SC": "Clayey Sand",
            "SM": "Silty Sand",
            "SW": "Well-graded Sand",
            "SP": "Poorly-graded Sand",
            "GW": "Well-graded Gravel",
            "GP": "Poorly-graded Gravel",
            "GM": "Silty Gravel",
            "GC": "Clayey Gravel"
        }
        return mapping.get(code, "Unknown Soil Type")

    ll = st.number_input("Liquid Limit (%)", value=40.0)
    pl = st.number_input("Plastic Limit (%)", value=25.0)

    if st.button("Classify Soil"):
        result = clf.predict([[ll, pl]])
        predicted_label = label_encoder.inverse_transform(result)[0]
        full_name = get_full_form(predicted_label)
        st.success(f"Predicted Soil Type: {predicted_label} - {full_name}")

# ---------------- Specific Gravity of Cement ----------------
elif option == "Specific Gravity of Cement":
    st.header("Specific Gravity of Cement Calculator")
    st.markdown("All weights should be in **grams (g)**. Specific gravity is in **g/cc**.")
    st.markdown("**Formula:** SG = (W2 - W1) / ((W2 - W1) - (W3 - W4)) × SG of Medium")

    w1 = st.number_input("Weight of Empty Flask (W1)", value=135.0)
    w2 = st.number_input("Weight of Flask + Cement (W2)", value=185.0)
    w3 = st.number_input("Weight of Flask + Cement + Medium (W3)", value=390.0)
    w4 = st.number_input("Weight of Flask + Medium (W4)", value=348.0)

    medium = st.selectbox("Select Medium", ["Kerosene", "Diesel"])
    sg_medium = 0.79 if medium == "Kerosene" else 0.83

    if st.button("Calculate Specific Gravity"):
        try:
            numerator = w2 - w1
            denominator = ((w2 - w1) - (w3 - w4)) * sg_medium
            specific_gravity = numerator / denominator
            st.success(f"Specific Gravity = {specific_gravity:.2f} g/cc")
        except ZeroDivisionError:
            st.error("Invalid inputs: Division by zero.")
