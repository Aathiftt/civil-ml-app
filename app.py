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

option = st.sidebar.selectbox("Select Tool", [
    "Concrete Strength Calculator", 
    "Soil Classification", 
    "Specific Gravity of Cement",
    "Area Converter"
])

# ---------------- Concrete Strength Calculator ----------------
if option == "Concrete Strength Calculator":
    st.header("Concrete Strength from CTM Reading")
    shape = st.selectbox("Select Shape of Specimen", ["Rectangle", "Circle", "Triangle"])

    if shape == "Rectangle":
        length = st.number_input("Enter Length (mm)", min_value=0.0, step=1.0)
        breadth = st.number_input("Enter Breadth (mm)", min_value=0.0, step=1.0)
        area = length * breadth

    elif shape == "Circle":
        radius = st.number_input("Enter Radius (mm)", min_value=0.0, step=1.0)
        area = 3.1416 * radius * radius

    elif shape == "Triangle":
        base = st.number_input("Enter Base (mm)", min_value=0.0, step=1.0)
        height = st.number_input("Enter Height (mm)", min_value=0.0, step=1.0)
        area = 0.5 * base * height

    ctm = st.number_input("Enter CTM Reading (Tonnes)", min_value=0.0, step=0.1)

    if st.button("Calculate Strength"):
        if area == 0:
            st.error("Area cannot be zero. Please enter valid dimensions.")
        else:
            force_n = ctm * 1000 * 9.81  # Convert ton to Newton
            strength = force_n / area  # MPa = N/mm²
            st.success(f"Area = {area:.2f} mm²")
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

    w1 = st.number_input("Weight of Empty Flask (W1)", value=0)
    w2 = st.number_input("Weight of Flask + Cement (W2)", value=0)
    w3 = st.number_input("Weight of Flask + Cement + Medium (W3)", value=0)
    w4 = st.number_input("Weight of Flask + Medium (W4)", value=0)

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
            
# ---------------- Area Converter ----------------
elif option == "Area Converter":
    st.header("Area Calculator & Converter")
    st.markdown("Calculate area in square meters and convert it to **cents** and **square feet**.")

    shape = st.selectbox("Select Shape", ["Rectangle", "Triangle", "Circle"])

    if shape == "Rectangle":
        length = st.number_input("Enter Length (m)", min_value=0.0)
        width = st.number_input("Enter Width (m)", min_value=0.0)
        area_m2 = length * width

    elif shape == "Triangle":
        base = st.number_input("Enter Base (m)", min_value=0.0)
        height = st.number_input("Enter Height (m)", min_value=0.0)
        area_m2 = 0.5 * base * height

    elif shape == "Circle":
        radius = st.number_input("Enter Radius (m)", min_value=0.0)
        area_m2 = 3.1416 * radius ** 2

    if st.button("Calculate Area"):
        area_cent = area_m2 / 40.47
        area_ft2 = area_m2 * 10.7639

# ---------------- Consistency Limit ----------------
st.markdown("---")
st.header("Consistency Limit Calculation")

consistency_option = st.selectbox("Select the type of limit to calculate:", ["Liquid Limit", "Plastic Limit", "Shrinkage Limit"])

if consistency_option == "Liquid Limit":
    st.subheader("Liquid Limit - Casagrande Method")
    st.markdown("**Description:** The Casagrande method determines the moisture content at which soil changes from plastic to liquid state. It involves placing soil in a Casagrande cup and recording the number of blows required to close a groove.")

    st.markdown("### Sample 1")
    m1_1 = st.number_input("Sample 1 - Mass of container (g)", key="ll_m1_1")
    m2_1 = st.number_input("Sample 1 - Mass of container + wet soil (g)", key="ll_m2_1")
    m3_1 = st.number_input("Sample 1 - Mass of container + dry soil (g)", key="ll_m3_1")
    n1 = st.number_input("Sample 1 - Number of blows", key="ll_n1")

    st.markdown("### Sample 2")
    m1_2 = st.number_input("Sample 2 - Mass of container (g)", key="ll_m1_2")
    m2_2 = st.number_input("Sample 2 - Mass of container + wet soil (g)", key="ll_m2_2")
    m3_2 = st.number_input("Sample 2 - Mass of container + dry soil (g)", key="ll_m3_2")
    n2 = st.number_input("Sample 2 - Number of blows", key="ll_n2")

    if st.button("Calculate Liquid Limit"):
        try:
            w1 = ((m2_1 - m3_1) / (m3_1 - m1_1)) * 100
            w2 = ((m2_2 - m3_2) / (m3_2 - m1_2)) * 100
            flow_index = (w1 - w2) / math.log10(n2 / n1)
            st.success(f"Water Content of Sample 1: {w1:.2f}%")
            st.success(f"Water Content of Sample 2: {w2:.2f}%")
            st.success(f"Flow Index (FI): {flow_index:.2f}")
        except:
            st.error("Check that none of the denominators are zero and all values are entered correctly.")

if consistency_option == "Plastic Limit":
    st.subheader("Plastic Limit")
    st.markdown("**Description:** The plastic limit is the moisture content at which soil can be rolled into threads without crumbling.")

    m1 = st.number_input("Mass of container (g)", key="pl_m1")
    m2 = st.number_input("Mass of container + wet soil (g)", key="pl_m2")
    m3 = st.number_input("Mass of container + dry soil (g)", key="pl_m3")

    if st.button("Calculate Plastic Limit"):
        try:
            pl = ((m2 - m3) / (m3 - m1)) * 100
            st.success(f"Plastic Limit (PL): {pl:.2f}%")
        except:
            st.error("Invalid input or division by zero.")

if consistency_option == "Shrinkage Limit":
    st.subheader("Shrinkage Limit")
    st.markdown("**Description:** The shrinkage limit is the moisture content below which further loss of moisture does not result in volume reduction.")

    m1 = st.number_input("Mass of shrinkage dish (g)", key="sl_m1")
    m2 = st.number_input("Mass of dish + wet soil (g)", key="sl_m2")
    m3 = st.number_input("Mass of dish + dry soil (g)", key="sl_m3")
    m4 = st.number_input("Mass of displaced mercury (g)", key="sl_m4")
    m5 = st.number_input("Mass of dish filled with mercury (g)", key="sl_m5")

    if st.button("Calculate Shrinkage Limit"):
        try:
            mass_water = m2 - m3
            volume_dry = m5 - m4
            sl = ((mass_water - (m3 - m1)) / volume_dry) * 100
            st.success(f"Shrinkage Limit (SL): {sl:.2f}%")
        except:
            st.error("Check the inputs. Ensure no division by zero or missing values.")

# ---------------- Final Soil Indices ----------------
st.markdown("---")
st.subheader("Additional Soil Indices")

ll = st.number_input("Enter Liquid Limit (LL) %", key="final_ll")
pl = st.number_input("Enter Plastic Limit (PL) %", key="final_pl")
sl = st.number_input("Enter Shrinkage Limit (SL) %", key="final_sl")
fi = st.number_input("Enter Flow Index (FI)", key="final_fi")
w_nat = st.number_input("Enter Natural Water Content (%)", key="natural_wc")

if st.button("Calculate Indices"):
    try:
        pi = ll - pl
        li = (w_nat - pl) / pi if pi != 0 else 0
        ti = pi / fi if fi != 0 else 0
        ci = (ll - w_nat) / pi if pi != 0 else 0
        si = pi - sl

        st.success(f"Plasticity Index (PI): {pi:.2f}%")
        st.success(f"Liquidity Index (LI): {li:.2f}")
        st.success(f"Toughness Index (TI): {ti:.2f}")
        st.success(f"Consistency Index (CI): {ci:.2f}")
        st.success(f"Shrinkage Index (SI): {si:.2f}%")
    except Exception as e:
        st.error(f"Error in calculation: {e}")


        st.success(f"Area = {area_m2:.2f} m²")
        st.info(f"In Cents: {area_cent:.2f} cents")
        st.info(f"In Square Feet: {area_ft2:.2f} ft²")

