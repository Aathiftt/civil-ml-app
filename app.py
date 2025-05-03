import streamlit as st
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", ["Concrete Strength Predictor", "Soil Classification"])

# -------------------- Concrete Strength Predictor ------------------------
if option == "Concrete Strength Predictor":
    st.header("Concrete Strength Predictor (Based on CTM Value and Area)")

    # Inputs for CTM and Area
    area = st.number_input("Area (m²)", value=1.0)
    ctm_value = st.number_input("CTM Value (Tonn)", value=10.0)

    # Button to calculate
    if st.button("Calculate Concrete Strength"):
        # Convert CTM value from tons to N (1 ton = 1000 kg, and 1 kg = 9.81 N)
        force = ctm_value * 1000 * 9.81  # Force in Newtons

        # Calculate the compressive strength (MPa) using the formula: strength = force / area
        strength = force / area  # Compressive strength in MPa

        st.success(f"Predicted Concrete Compressive Strength: {strength:.2f} MPa")

# -------------------- Soil Classification ------------------------
elif option == "Soil Classification":
    st.header("Soil Classification Based on Index Properties")

    # Example dataset
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

    # Mapping soil types to full forms
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

    # User inputs
    ll = st.number_input("Liquid Limit (%)", value=40.0)
    pl = st.number_input("Plastic Limit (%)", value=25.0)

    # Button to calculate
    if st.button("Classify Soil Type"):
        result = clf.predict([[ll, pl]])
        predicted_label = label_encoder.inverse_transform(result)[0]
        full_name = get_full_form(predicted_label)

        st.success(f"Predicted Soil Type: {predicted_label} - {full_name}")
