import streamlit as st
import numpy as np

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", ["Concrete Strength Predictor", "Soil Classification"])

# -------------------- Concrete Strength Predictor ------------------------
if option == "Concrete Strength Predictor":
    st.header("Concrete Strength Predictor (Based on CTM Value and Area in mm²)")

    # Inputs for CTM and Area (Area is in mm²)
    area_mm = st.number_input("Area (mm²)", value=19475)
    ctm_value = st.number_input("CTM Value (Tonn)", value=7.8)

    # Button to calculate
    if st.button("Calculate Concrete Strength"):
        # Convert CTM value from tons to Force in Newtons
        # 1 ton = 1000 kg, 1 kg = 9.81 N
        force = ctm_value * 1000 * 9.81  # Force in Newtons

        # Calculate the compressive strength (MPa) using the formula: strength = force / area
        strength = force / area_mm  # Compressive strength in MPa (since 1 MPa = 1 N/mm²)

        st.success(f"Predicted Concrete Compressive Strength: {strength:.2f} MPa")

# -------------------- Soil Classification ------------------------
elif option == "Soil Classification":
    st.header("Soil Classification Based on Index Properties")

    # Example dataset for soil classification
    soil_data = {
        "Liquid Limit": [30, 60, 45, 40, 50, 35],
        "Plastic Limit": [20, 25, 30, 28, 33, 24],
        "Soil Type": ["CL", "CH", "CL", "CL", "CH", "CL"]
    }

    # Ensure soil_data is correctly converted to a DataFrame
    df = pd.DataFrame(soil_data)

    # Define features and target
    X = df[["Liquid Limit", "Plastic Limit"]]
    y = df["Soil Type"]

    # Encoding labels for classification
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

    # User inputs for soil classification
    ll = st.number_input("Liquid Limit (%)", value=40.0)
    pl = st.number_input("Plastic Limit (%)", value=25.0)

    # Button to calculate
    if st.button("Classify Soil Type"):
        result = clf.predict([[ll, pl]])
        predicted_label = label_encoder.inverse_transform(result)[0]
        full_name = get_full_form(predicted_label)

        st.success(f"Predicted Soil Type: {predicted_label} - {full_name}")
