import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", ["Concrete Strength Predictor", "Soil Classification", "Specific Gravity of Cement"])

# -------------------- Concrete Strength Predictor ------------------------
if option == "Concrete Strength Predictor":
    st.header("Concrete Strength Predictor")

    st.subheader("Input")
    area = st.number_input("Area of Specimen (mm²)", value=2250.0, format="%.2f")
    ctm_reading = st.number_input("CTM Reading (tonnes)", value=7.5, format="%.2f")

    if st.button("Calculate Compressive Strength"):
        force_n = ctm_reading * 1000 * 9.81  # Convert tonnes to Newtons
        strength_mpa = force_n / area  # 1 MPa = 1 N/mm²
        st.success(f"Compressive Strength: {strength_mpa:.2f} MPa")

# -------------------- Soil Classification ------------------------
elif option == "Soil Classification":
    st.header("Soil Classification Based on Index Properties")

    # Sample data
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

# -------------------- Specific Gravity of Cement ------------------------
elif option == "Specific Gravity of Cement":
    st.header("Specific Gravity of Cement")
    st.markdown("**All weights must be in grams (g). Output unit: g/cc**")

    medium = st.selectbox("Select Medium", ["Kerosene", "Diesel"])
    sg_medium = 0.79 if medium == "Kerosene" else 0.83

    w1 = st.number_input("Weight of empty flask (W1) [g]", value=135.0)
    w2 = st.number_input("Weight of flask + cement (W2) [g]", value=185.0)
    w3 = st.number_input("Weight of flask + cement + medium (W3) [g]", value=390.0)
    w4 = st.number_input("Weight of flask + medium only (W4) [g]", value=348.0)

    if st.button("Calculate Specific Gravity"):
        try:
            numerator = w2 - w1
            denominator = (w2 - w1) - ((w3 - w4) * sg_medium)
            if denominator == 0:
                st.error("Division by zero in denominator. Check your values.")
            else:
                sg_cement = numerator / denominator
                st.success(f"Specific Gravity of Cement = {sg_cement:.2f} g/cc")
        except Exception as e:
            st.error(f"Error in calculation: {e}")
