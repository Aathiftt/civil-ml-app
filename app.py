import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from scipy.interpolate import interp1d

st.set_page_config(page_title="Civil Engineering Calculator", layout="wide")
st.title("🧱 Civil Engineering Lab Assistant")
st.subheader("Welcome to the Civil Engineering Analysis Toolkit")

MODULES = [
    "Home",
    "Strength of Materials",
    "Soil Classification",
    "Specific Gravity of Cement",
    "Sieve Analysis",
    "Area Converter"
]

option = st.sidebar.selectbox("Choose a module", MODULES)

def number_input_row(labels, keys=None, min_value=0.0):
    """Helper to create a row of number inputs and return their values."""
    cols = st.columns(len(labels))
    values = []
    for i, label in enumerate(labels):
        key = keys[i] if keys else label
        values.append(cols[i].number_input(label, min_value=min_value, key=key))
    return values

if option == "Home":
    st.markdown("""
    This web application is designed to assist students, educators, and professionals in performing common civil engineering lab computations and visualizations with ease.

    ### 💡 Features:
    - Calculate Various Strengths from Applied Load Data
    - Analyze **Soil Properties** from index limits
    - Calculate **Consistency Limits** for classification
    - Calculate **Specific Gravity** of cement using Le Chatlier Apparatus
    - Perform **Sieve Analysis** and plot **Particle Size Distribution**
    - Calculate and Convert Area of a plot
    - Get instant insights and basic soil classification

    ### 🔍 How to Use:
    1. Select a module from the left sidebar.
    2. Enter your data in the provided fields.
    3. View results instantly with charts or classifications.
    4. Use sample values (if unsure) to try out the modules.
    5. Print the Result using the **Print** Option at top right : Icon

    👉 Explore each section using the sidebar. Happy Testing!  
    """)

# ---------------- Strength of Materials ----------------
elif option == "Strength of Materials":
    st.header("Strength of Materials")
    strength_type = st.selectbox("Select Type of Strength", 
                                 ["Compressive Strength", "Tensile Strength", "Transverse Strength of Tile"])

    if strength_type == "Compressive Strength":
        shape = st.selectbox("Choose Shape of Specimen", ["Rectangle", "Circle"])
        if shape == "Rectangle":
            length, breadth = number_input_row(["Enter Length (mm)", "Enter Breadth (mm)"])
            area = length * breadth
        else:
            radius = st.number_input("Enter Radius (mm)", min_value=0.0)
            area = math.pi * radius ** 2
        ctm = st.number_input("Enter CTM Reading (Tonnes)", min_value=0.0)
        if st.button("Calculate Strength"):
            if area > 0:
                force_n = ctm * 1000 * 9.81
                strength = force_n / area
                st.success(f"Compressive Strength = {strength:.2f} N/mm²")
            else:
                st.error("Area must be greater than 0.")

    elif strength_type == "Tensile Strength":
        p, d, l = number_input_row(
            ["Enter Load from CTM (Tonnes)", "Enter Diameter of Cylinder (mm)", "Enter Length of Cylinder (mm)"]
        )
        if st.button("Calculate Strength"):
            if d > 0 and l > 0:
                force_n = p * 1000 * 9.81
                strength = (2 * force_n) / (math.pi * d * l)
                st.success(f"Tensile Strength = {strength:.2f} N/mm²")
            else:
                st.error("Diameter and Length must be greater than 0.")

    elif strength_type == "Transverse Strength of Tile":
        p, f, l, b, t = number_input_row(
            ["Enter Breaking Load (kg)", "Enter Length of Lever Arm (mm)", "Enter Length of Specimen (mm)", 
             "Enter Breadth (mm)", "Enter Thickness (mm)"]
        )
        if st.button("Calculate Strength"):
            if b > 0 and t > 0:
                p_n = p * 9.81
                strength = (3 * p_n * f * l) / (2 * b * t ** 2)
                st.success(f"Transverse Strength = {strength:.2f} N/mm²")
            else:
                st.error("Breadth and Thickness must be greater than 0.")

# ---------------- Soil Classification ----------------
elif option == "Soil Classification":
    st.header("Soil Classification Tools")
    consistency_option = st.selectbox("Choose Consistency Limit Type", ["None", "Liquid Limit", "Plastic Limit", "Shrinkage Limit"])

    if consistency_option == "Liquid Limit":
        st.subheader("Liquid Limit - Casagrande Method")
        st.markdown("**Description:** The Casagrande method determines the moisture content at which soil changes from plastic to liquid state.")

        st.markdown("### Sample 1")
        m1_1, m2_1, m3_1, n1 = number_input_row(
            ["Mass of container (g)", "Mass of container + wet soil (g)", "Mass of container + dry soil (g)", "Number of blows"],
            keys=["ll_m1_1", "ll_m2_1", "ll_m3_1", "ll_n1"]
        )
        st.markdown("### Sample 2")
        m1_2, m2_2, m3_2, n2 = number_input_row(
            ["Mass of container (g)", "Mass of container + wet soil (g)", "Mass of container + dry soil (g)", "Number of blows"],
            keys=["ll_m1_2", "ll_m2_2", "ll_m3_2", "ll_n2"]
        )

        if st.button("Calculate Liquid Limit"):
            try:
                w1 = ((m2_1 - m1_1) - (m3_1 - m1_1)) / (m3_1 - m1_1) * 100
                w2 = ((m2_2 - m1_2) - (m3_2 - m1_2)) / (m3_2 - m1_2) * 100
                flow_index = (w1 - w2) / math.log10(n2 / n1)
                liquid_limit = (w1 + w2) / 2
                st.success(f"Water content Sample 1 = {w1:.2f}%")
                st.success(f"Water content Sample 2 = {w2:.2f}%")
                st.success(f"Liquid Limit = {liquid_limit:.2f}%")
                st.success(f"Flow Index = {flow_index:.2f}")
            except Exception:
                st.error("Check that none of the denominators are zero and all values are entered correctly.")

    elif consistency_option == "Plastic Limit":
        st.subheader("Plastic Limit")
        st.markdown("**Description:** The plastic limit is the water content at which soil changes from plastic to semi-solid state.")
        m1, m2, m3 = number_input_row(
            ["Mass of container (g)", "Mass of container + wet soil (g)", "Mass of container + dry soil (g)"],
            keys=["pl_m1", "pl_m2", "pl_m3"]
        )
        if st.button("Calculate Plastic Limit"):
            try:
                plastic_limit = ((m2 - m1) - (m3 - m1)) / (m3 - m1) * 100
                st.success(f"Plastic Limit = {plastic_limit:.2f}%")
            except Exception:
                st.error("Invalid input values.")

    elif consistency_option == "Shrinkage Limit":
        st.subheader("Shrinkage Limit")
        st.markdown("**Description:** The shrinkage limit is the maximum water content at which a reduction in water content does not cause a decrease in the volume of a soil sample.")
        m1, m2, m3, mercury_dish, mercury_disp = number_input_row(
            ["Mass of shrinkage dish (g)", "Mass of shrinkage dish + wet soil (g)", "Mass of shrinkage dish + dry soil (g)",
             "Mass of dish filled with mercury (g)", "Weight of mercury after displacement (g)"],
            keys=["sl_m1", "sl_m2", "sl_m3", "sl_mercury_dish", "sl_mercury_disp"]
        )
        if st.button("Calculate Shrinkage Limit"):
            try:
                mass_water = (m2 - m3)
                mass_dry = (m3 - m1)
                volume_dry = mercury_dish - mercury_disp
                shrinkage_limit = ((mass_water - volume_dry) / mass_dry) * 100
                st.success(f"Shrinkage Limit = {shrinkage_limit:.2f}%")
            except Exception:
                st.error("Invalid input values.")

    # Indices calculation
    st.subheader("Calculate Other Indices")
    st.markdown("Please input the values for Liquid Limit (LL), Plastic Limit (PL), Shrinkage Limit (SL), and Natural Water Content (WC) to calculate the indices:")
    LL, PL, SL, WC = number_input_row(
        ["Enter Liquid Limit (LL) (%)", "Enter Plastic Limit (PL) (%)", "Enter Shrinkage Limit (SL) (%)", "Enter Natural Water Content (WC) (%)"]
    )
    if st.button("Calculate Indices"):
        if LL <= PL:
            st.error("Liquid Limit must be greater than Plastic Limit.")
        else:
            PI = LL - PL
            LI = (WC - PL) / PI if PI != 0 else 0
            CI = (LL - WC) / PI if PI != 0 else 0
            SI = LL - SL
            st.success(f"Plasticity Index (PI) = {PI:.2f}")
            st.success(f"Liquidity Index (LI) = {LI:.2f}")
            st.success(f"Consistency Index (CI) = {CI:.2f}")
            st.success(f"Shrinkage Index (SI) = {SI:.2f}")

# ---------------- Specific Gravity of Cement ----------------
elif option == "Specific Gravity of Cement":
    st.header("Specific Gravity of Cement")
    st.markdown("All weights must be entered in grams (g). Result unit: g/cc")
    medium = st.selectbox("Select Medium", ["Kerosene", "Diesel"])
    sg_medium = 0.79 if medium == "Kerosene" else 0.83
    w1, w2, w3, w4 = number_input_row(
        ["Weight of empty flask (g)", "Weight of flask + cement (g)", 
         "Weight of flask + cement + medium (g)", "Weight of flask + medium (g)"]
    )
    if st.button("Calculate Specific Gravity"):
        try:
            specific_gravity = (w2 - w1) / ((w2 - w1) - (w3 - w4)) * sg_medium
            st.success(f"Specific Gravity = {specific_gravity:.2f} g/cc")
        except Exception:
            st.error("Ensure all weights are entered and denominator is not zero.")

# ---------------- Area Converter ----------------
elif option == "Area Converter":
    st.header("Area Calculator and Converter")
    shape = st.selectbox("Select Shape", ["Rectangle", "Triangle", "Circle"])
    area_m2 = 0
    if shape == "Rectangle":
        length, width = number_input_row(["Enter Length (m)", "Enter Width (m)"])
        area_m2 = length * width
    elif shape == "Triangle":
        base, height = number_input_row(["Enter Base (m)", "Enter Height (m)"])
        area_m2 = 0.5 * base * height
    elif shape == "Circle":
        radius = st.number_input("Enter Radius (m)", min_value=0.0)
        area_m2 = math.pi * radius ** 2
    if st.button("Convert Area"):
        cents = area_m2 / 40.47
        sq_feet = area_m2 * 10.7639
        st.success(f"Area in m²: {area_m2:.2f} m²")
        st.info(f"Area in cents: {cents:.2f} cents")
        st.info(f"Area in square feet: {sq_feet:.2f} ft²")

# -------------------- Sieve Analysis ------------------------
elif option == "Sieve Analysis":
    st.header("Sieve Analysis and PSD Chart")
    material_type = st.selectbox("Select Material Type", ["Soil", "Aggregates"])
    num_sieves = st.number_input("Enter number of sieves", min_value=2, max_value=10, value=5)

    st.subheader("Enter sieve details")
    standard_sieves = ['80mm','63mm','50mm','40mm','37.5mm','31.5','25mm','20mm','12.5mm','10mm','6.3mm','4.75 mm', '2.36 mm', '1.18 mm', '600 µm', '300 µm', '150 µm', '75 µm']
    sieve_sizes, retained_percents = [], []

    for i in range(int(num_sieves)):
        col1, col2 = st.columns(2)
        with col1:
            sieve = st.selectbox(f"Select sieve {i+1}", standard_sieves, key=f"sieve_{i}")
        with col2:
            retained = st.number_input(f"% Retained on {sieve}", min_value=0.0, max_value=100.0, value=0.0, key=f"ret_{i}")
        sieve_val = float(sieve.replace("mm", "").replace("µm", "").strip())
        if "µm" in sieve:
            sieve_val /= 1000
        sieve_sizes.append(sieve_val)
        retained_percents.append(retained)

    if st.button("Analyze"):
        df = pd.DataFrame({
            "Sieve Size (mm)": sieve_sizes,
            "% Retained": retained_percents
        }).sort_values("Sieve Size (mm)", ascending=False)
        df["Cumulative Retained"] = df["% Retained"].cumsum()
        df["% Passing"] = 100 - df["Cumulative Retained"]
        st.subheader("Sieve Analysis Table")
        st.dataframe(df)

        fig, ax = plt.subplots()
        ax.plot(df["Sieve Size (mm)"], df["% Passing"], marker='o', linestyle='-')
        ax.set_xscale('log')
        ax.invert_xaxis()
        ax.set_xlabel("Sieve Size (mm, log scale)")
        ax.set_ylabel("% Passing")
        ax.set_title("Particle Size Distribution Curve")
        ax.grid(True, which='both')
        st.pyplot(fig)

        if material_type == "Soil":
            sieve_4_75_index = df[np.isclose(df["Sieve Size (mm)"], 4.75)].index
            if not sieve_4_75_index.empty:
                percent_passing_4_75 = df.loc[sieve_4_75_index[0], "% Passing"]
                if percent_passing_4_75 > 50:
                    st.info("Soil appears to be fine-grained (more than 50% passing through 4.75 mm sieve).")
                else:
                    st.info("Soil appears to be coarse-grained (less than 50% passing through 4.75 mm sieve).")
            else:
                st.warning("4.75 mm sieve not included in input. Cannot determine basic soil type.")

            try:
                interp_func = interp1d(df["% Passing"][::-1], df["Sieve Size (mm)"][::-1], kind='linear', bounds_error=False, fill_value="extrapolate")
                D10 = float(interp_func(10))
                D30 = float(interp_func(30))
                D60 = float(interp_func(60))
                Cu = round(D60 / D10, 2)
                Cc = round((D30**2) / (D10 * D60), 2)
                st.subheader("Soil Gradation Parameters")
                st.markdown(f"- D10 (Effective Size): **{D10:.2f} mm**")
                st.markdown(f"- D30: **{D30:.2f} mm**")
                st.markdown(f"- D60: **{D60:.2f} mm**")
                st.markdown(f"- Uniformity Coefficient (Cu): **{Cu}**")
                st.markdown(f"- Coefficient of Curvature (Cc): **{Cc}**")
                if Cu < 4 or Cc < 1 or Cc > 3:
                    st.info("Soil appears to be poorly graded.")
                else:
                    st.info("Soil appears to be well graded.")
            except Exception:
                st.warning("Not enough data to calculate D10, D30, D60. Ensure data covers relevant passing percentages.")
