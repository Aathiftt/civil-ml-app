import streamlit as st
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", [
    "Concrete Strength Predictor",
    "Soil Classification",
    "Specific Gravity of Cement"
])

# -------------------- Concrete Strength Predictor ------------------------
if option == "Concrete Strength Predictor":
    st.header("Concrete Strength Predictor (Area in mm²)")

    area_mm = st.number_input("Area (mm²)", value=19475)
    ctm_value = st.number_input("CTM Value (Tonn)", value=7.8)

    if st.button("Calculate Concrete Strength"):
        force = ctm_value * 1000 * 9.81  # ton to N
        strength = force / area_mm       # MPa = N/mm²
        st.success(f"Predicted Concrete Compressive Strength: {strength:.2f} MPa")

# -------------------- Soil Classification ------------------------
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

    if st.button("Classify Soil Type"):
        result = clf.predict([[ll, pl]])
        predicted_label = label_encoder.inverse_transform(result)[0]
        full_name = get_full_form(predicted_label)
        st.success(f"Predicted Soil Type: {predicted_label} - {full_name}")

# -------------------- Specific Gravity of Cement ------------------------
elif option == "Specific Gravity of Cement":
    st.header("Specific Gravity of Cement")

    w1 = st.number_input("Weight of empty flask (W1)", value=0.0)
    w2 = st.number_input("Weight of flask + cement (W2)", value=0.0)
    w3 = st.number_input("Weight of flask + cement + medium (W3)", value=0.0)
    w4 = st.number_input("Weight of flask filled with medium only (W4)", value=0.0)

    medium = st.selectbox("Select Medium", ["Kerosene", "Diesel"])
    medium_sp_gravity = 0.79 if medium == "Kerosene" else 0.83

    if st.button("Calculate Specific Gravity"):
        try:
            numerator = w2 - w1
            denominator = (w2 - w1) - (w3 - w4)
            if denominator == 0:
                st.error("Denominator is zero. Please check input values.")
            else:
                sp_gravity = numerator / (denominator * medium_sp_gravity)
                st.success(f"Specific Gravity of Cement using {medium}: {sp_gravity:.3f}")
        except Exception as e:
            st.error(f"Error in calculation. Details: {e}")
