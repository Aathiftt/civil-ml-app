import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Civil Lab Assistant", layout="centered")

# Initialize session state
if "option" not in st.session_state:
    st.session_state.option = "Home"

st.markdown("""
    <style>
        .css-1n7v3ny {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 8px 12px;
            font-size: 16px;
            border: 1px solid #ddd;
            transition: all 0.3s ease;
        }

        .css-1n7v3ny:focus {
            outline: none;
            border: 1px solid #ff4b4b;
            box-shadow: 0px 0px 10px rgba(255, 75, 75, 0.6);
        }

        .stSelect div.stSelectMenu {
            max-height: 200px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: #ff4b4b transparent;
        }

        .stSelect div.stSelectMenu::-webkit-scrollbar {
            width: 8px;
        }

        .stSelect div.stSelectMenu::-webkit-scrollbar-thumb {
            background: #ff4b4b;
            border-radius: 4px;
        }

        .stSelect div.stSelectMenu::-webkit-scrollbar-track {
            background: transparent;
        }
    </style>
""", unsafe_allow_html=True)

# Page UI
st.title("🧱 Civil Engineering Lab Assistant")
st.subheader("Welcome to the Civil Engineering Analysis Toolkit")

# Dropdown and session state handling
selected_option = st.selectbox(
    "Select a Module", 
    ["Home", "Strength of Materials", "Soil Classification", "Workability", 
     "Specific Gravity of Cement", "Sieve Analysis", "Area Converter", "Bitumen Analysis"]
)

st.session_state.option = selected_option
option = st.session_state.option

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
    
    👉 Explore each section using the dropdown bar above. Happy Testing!  
    """)

    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <a href="mailto:aathiftt@gmail.com?subject=Issue%20Report%20-%20Civil%20Lab%20Web%20App&body=Please%20describe%20the%20issue%20you%20faced%20in%20detail%20below:"
           style="display: inline-block; padding: 0.6em 1.2em; font-size: 16px; background-color: #ff4b4b; color: white; border-radius: 5px; text-decoration: none;">
            🐞 Report an Issue
        </a>
    </div>
    <div style="text-align: center; margin-top: 10px; font-size: 14px; color: #ff4b4b;">
        <p><strong>Note:</strong> This button works only with Android/iOS devices.</p>
    </div>
    """, unsafe_allow_html=True)


# ----------------Strength of Materials Calculator ----------------

if option == "Strength of Materials":
    st.header("Strength of Materials")

    strength_type = st.selectbox("Select Type of Strength", 
                                 ["Compressive Strength", "Tensile Strength", "Transverse Strength of Tile"])

    if strength_type == "Compressive Strength":
        shape = st.selectbox("Choose Shape of Specimen", ["Rectangle", "Circle"])

        if shape == "Rectangle":
            length = st.number_input("Enter Length (mm)", min_value=0.0)
            breadth = st.number_input("Enter Breadth (mm)", min_value=0.0)
            area = length * breadth
        elif shape == "Circle":
            radius = st.number_input("Enter Radius (mm)", min_value=0.0)
            area = math.pi * radius * radius

        ctm = st.number_input("Enter CTM Reading (Tonnes)", min_value=0.0)

        if st.button("Calculate Strength"):
            if area > 0:
                force_n = ctm * 1000 * 9.81
                strength = force_n / area
                st.success(f"Compressive Strength = {strength:.2f} N/mm²")
            else:
                st.error("Area must be greater than 0.")

    elif strength_type == "Tensile Strength":
        p = st.number_input("Enter Load from CTM (Tonnes)", min_value=0.0)
        d = st.number_input("Enter Diameter of Cylinder (mm)", min_value=0.0)
        l = st.number_input("Enter Length of Cylinder (mm)", min_value=0.0)

        if st.button("Calculate Strength"):
            if d > 0 and l > 0:
                force_n = p * 1000 * 9.81
                strength = (2 * force_n) / (math.pi * d * l)
                st.success(f"Tensile Strength = {strength:.2f} N/mm²")
            else:
                st.error("Diameter and Length must be greater than 0.")

    elif strength_type == "Transverse Strength of Tile":
        p = st.number_input("Enter Breaking Load (kg)", min_value=0.0)
        f = st.number_input("Enter Length of Lever Arm (mm)", min_value=0.0)
        l = st.number_input("Enter Length of Specimen (mm)", min_value=0.0)
        b = st.number_input("Enter Breadth (mm)", min_value=0.0)
        t = st.number_input("Enter Thickness (mm)", min_value=0.0)

        if st.button("Calculate Strength"):
            if b > 0 and t > 0:
                p_n = p * 9.81  # convert kg to Newtons
                strength = (3 * p_n * f * l) / (2 * b * t * t)
                st.success(f"Transverse Strength = {strength:.2f} N/mm²")
            else:
                st.error("Breadth and Thickness must be greater than 0.")

# ---------------- Soil Classification ----------------
elif option == "Soil Classification":
    st.header("Soil Classification Tools")

    consistency_option = st.selectbox("Choose Consistency Limit Type", ["None", "Liquid Limit", "Plastic Limit", "Shrinkage Limit"])

    liquid_limit = plastic_limit = shrinkage_limit = None

    if consistency_option == "Liquid Limit":
        st.subheader("Liquid Limit - Casagrande Method")
        st.markdown("**Description:** The Casagrande method determines the moisture content at which soil changes from plastic to liquid state.")

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
                w1 = ((m2_1 - m1_1) - (m3_1 - m1_1)) / (m3_1 - m1_1) * 100
                w2 = ((m2_2 - m1_2) - (m3_2 - m1_2)) / (m3_2 - m1_2) * 100

                flow_index = (w1 - w2) / math.log10(n2 / n1)
                liquid_limit = (w1 + w2) / 2

                st.success(f"Water content Sample 1 = {w1:.2f}%")
                st.success(f"Water content Sample 2 = {w2:.2f}%")
                st.success(f"Liquid Limit = {liquid_limit:.2f}%")
                st.success(f"Flow Index = {flow_index:.2f}")
            except:
                st.error("Check that none of the denominators are zero and all values are entered correctly.")

    elif consistency_option == "Plastic Limit":
        st.subheader("Plastic Limit")
        st.markdown("**Description:** The plastic limit is the water content at which soil changes from plastic to semi-solid state.")

        m1 = st.number_input("Mass of container (g)", key="pl_m1")
        m2 = st.number_input("Mass of container + wet soil (g)", key="pl_m2")
        m3 = st.number_input("Mass of container + dry soil (g)", key="pl_m3")

        if st.button("Calculate Plastic Limit"):
            try:
                plastic_limit = ((m2 - m1) - (m3 - m1)) / (m3 - m1) * 100
                st.success(f"Plastic Limit = {plastic_limit:.2f}%")
            except:
                st.error("Invalid input values.")

    elif consistency_option == "Shrinkage Limit":
        st.subheader("Shrinkage Limit")
        st.markdown("**Description:** The shrinkage limit is the maximum water content at which a reduction in water content does not cause a decrease in the volume of a soil sample.")

        m1 = st.number_input("Mass of shrinkage dish (g)", key="sl_m1")
        m2 = st.number_input("Mass of shrinkage dish + wet soil (g)", key="sl_m2")
        m3 = st.number_input("Mass of shrinkage dish + dry soil (g)", key="sl_m3")
        mercury_dish = st.number_input("Mass of dish filled with mercury (g)", key="sl_mercury_dish")
        mercury_displaced = st.number_input("Weight of mercury after displacement (g)", key="sl_mercury_disp")

        if st.button("Calculate Shrinkage Limit"):
            try:
                mass_water = (m2 - m3)
                mass_dry = (m3 - m1)
                volume_dry = mercury_dish - mercury_displaced
                shrinkage_limit = ((mass_water - volume_dry) / mass_dry) * 100
                st.success(f"Shrinkage Limit = {shrinkage_limit:.2f}%")
            except:
                st.error("Invalid input values.")

    # ---------------- Additional Indices ----------------
    st.subheader("Calculate Other Indices")
    st.markdown("Please input the values for Liquid Limit (LL), Plastic Limit (PL), Shrinkage Limit (SL), and Natural Water Content (WC) to calculate the indices:")

    LL = st.number_input("Enter Liquid Limit (LL) (%)", min_value=0.0)
    PL = st.number_input("Enter Plastic Limit (PL) (%)", min_value=0.0)
    SL = st.number_input("Enter Shrinkage Limit (SL) (%)", min_value=0.0)
    WC = st.number_input("Enter Natural Water Content (WC) (%)", min_value=0.0)

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

    w1 = st.number_input("Weight of empty flask (g)")
    w2 = st.number_input("Weight of flask + cement (g)")
    w3 = st.number_input("Weight of flask + cement + medium (g)")
    w4 = st.number_input("Weight of flask + medium (g)")

    if st.button("Calculate Specific Gravity"):
        try:
            specific_gravity = (w2 - w1) / ((w2 - w1) - (w3 - w4)) * sg_medium
            st.success(f"Specific Gravity = {specific_gravity:.2f} g/cc")
        except:
            st.error("Ensure all weights are entered and denominator is not zero.")

# ---------------- Area Converter ----------------
elif option == "Area Converter":
    st.header("Area Calculator and Converter")
    shape = st.selectbox("Select Shape", ["Rectangle", "Triangle", "Circle"])

    area_m2 = 0

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

    # Select whether it's soil or aggregates
    material_type = st.selectbox("Select Material Type", ["Soil", "Aggregates"])

    num_sieves = st.number_input("Enter number of sieves", min_value=2, max_value=10, value=5)

    st.subheader("Enter sieve details")

    standard_sieves = ['80mm', '63mm', '50mm', '40mm', '37.5mm', '31.5', '25mm', '20mm', '12.5mm', '10mm', '6.3mm',
                       '4.75 mm', '2.36 mm', '1.18 mm', '600 µm', '300 µm', '150 µm', '75 µm']
    sieve_sizes = []
    retained_percents = []

    for i in range(int(num_sieves)):
        col1, col2 = st.columns(2)
        with col1:
            sieve = st.selectbox(f"Select sieve {i+1}", standard_sieves, key=f"sieve_{i}")
        with col2:
            retained = st.number_input(f"% Retained on {sieve}", min_value=0.0, max_value=100.0, value=0.0,
                                       key=f"ret_{i}")

        sieve_val = float(sieve.replace("mm", "").replace("µm", "").strip())
        if "µm" in sieve:
            sieve_val /= 1000  # Convert microns to mm
        sieve_sizes.append(sieve_val)
        retained_percents.append(retained)

    if st.button("Analyze"):
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import interp1d
        import pandas as pd

        df = pd.DataFrame({
            "Sieve Size (mm)": sieve_sizes,
            "% Retained": retained_percents
        })

        df.sort_values("Sieve Size (mm)", ascending=False, inplace=True)
        df["Cumulative Retained"] = df["% Retained"].cumsum()
        df["% Passing"] = 100 - df["Cumulative Retained"]

        st.subheader("Sieve Analysis Table")
        st.dataframe(df)

        # Plotting PSD curve
        fig, ax = plt.subplots()
        ax.plot(df["Sieve Size (mm)"], df["% Passing"], marker='o', linestyle='-')
        ax.set_xscale('log')
        ax.invert_xaxis()
        ax.set_xlabel("Sieve Size (mm, log scale)")
        ax.set_ylabel("% Passing")
        ax.set_title("Particle Size Distribution Curve")
        ax.grid(True, which='both')
        st.pyplot(fig)

        # Analysis based on material type
        if material_type == "Soil":
            # Classification as fine or coarse
            sieve_4_75_index = df[np.isclose(df["Sieve Size (mm)"], 4.75)].index
            if not sieve_4_75_index.empty:
                percent_passing_4_75 = df.loc[sieve_4_75_index[0], "% Passing"]
                if percent_passing_4_75 > 50:
                    st.info("Soil appears to be fine-grained (more than 50% passing through 4.75 mm sieve).")
                else:
                    st.info("Soil appears to be coarse-grained (less than 50% passing through 4.75 mm sieve).")
            else:
                st.warning("4.75 mm sieve not included in input. Cannot determine basic soil type.")

            # Gradation parameters
            try:
                interp_func = interp1d(df["% Passing"][::-1], df["Sieve Size (mm)"][::-1],
                                       kind='linear', bounds_error=False, fill_value="extrapolate")
                D10 = float(interp_func(10))
                D30 = float(interp_func(30))
                D60 = float(interp_func(60))
                Cu = round(D60 / D10, 2)
                Cc = round((D30 ** 2) / (D10 * D60), 2)

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
            except Exception as e:
                st.warning("Not enough data to calculate D10, D30, D60. Ensure data covers relevant passing percentages.")

        elif material_type == "Aggregates":
            # Classification as fine or coarse
            sieve_4_75_index = df[np.isclose(df["Sieve Size (mm)"], 4.75)].index
            if not sieve_4_75_index.empty:
                percent_passing_4_75 = df.loc[sieve_4_75_index[0], "% Passing"]
                if percent_passing_4_75 > 50:
                    st.info("Aggregates appear to be fine-grained (more than 50% passing through 4.75 mm sieve).")
                else:
                    st.info("Aggregates appear to be coarse-grained (less than 50% passing through 4.75 mm sieve).")
            else:
                st.warning("4.75 mm sieve not included in input. Cannot determine basic material type.")

            # Fineness Modulus (FM)
            try:
                fm = df["% Passing"].sum() / 100
                st.subheader("Fineness Modulus Calculation")
                st.markdown(f"- Fineness Modulus (FM): **{fm:.2f}**")

                if fm < 2.5:
                    zone = "Zone I"
                elif 2.5 <= fm <= 3.0:
                    zone = "Zone II"
                elif 3.0 < fm <= 3.5:
                    zone = "Zone III"
                else:
                    zone = "Zone IV"

                st.markdown(f"- Aggregate Zone: **{zone}**")
            except Exception as e:
                st.warning("Not enough data to calculate Fineness Modulus (FM). Ensure data covers relevant sieves.")

            # Gradation parameters for aggregates
            try:
                interp_func = interp1d(df["% Passing"][::-1], df["Sieve Size (mm)"][::-1],
                                       kind='linear', bounds_error=False, fill_value="extrapolate")
                D10 = float(interp_func(10))
                D30 = float(interp_func(30))
                D60 = float(interp_func(60))
                Cu = round(D60 / D10, 2)
                Cc = round((D30 ** 2) / (D10 * D60), 2)

                st.subheader("Grain Size Parameters")
                st.markdown(f"- D10 (Effective Size): **{D10:.2f} mm**")
                st.markdown(f"- D30: **{D30:.2f} mm**")
                st.markdown(f"- D60: **{D60:.2f} mm**")

                st.subheader("Uniformity and Curvature Coefficients")
                st.markdown(f"- Uniformity Coefficient : **{Cu}**")
                st.markdown(f"- Coefficient of Curvature : **{Cc}**")
            except Exception as e:
                st.warning("Not enough data to calculate D10, D30, D60 for aggregates.")

#-------------------workability-------------------
elif option == "Workability":
    st.header("Workability of Concrete")

    test_type = st.selectbox(
        "Select Workability Test",
        ["Slump Test", "Compaction Factor", "Flow Table", "Vee Bee"]
    )

    result_displayed = False

    if test_type == "Slump Test":
        slump_value = st.number_input("Enter Slump Value (mm)", min_value=0.0)
        if st.button("Analyze"):
            st.markdown(f"### Slump Value: **{slump_value:.1f} mm**")
            if slump_value < 25:
                st.success("Inference: The concrete shows **very low workability**, which is typically suitable for road construction or applications requiring very stiff mixes.")
            elif 25 <= slump_value < 50:
                st.success("Inference: The concrete has **low workability**, commonly used in mass concreting where vibration is employed.")
            elif 50 <= slump_value < 100:
                st.success("Inference: The concrete exhibits **medium workability**, appropriate for normal reinforced concrete placed with light compaction.")
            elif 100 <= slump_value <= 175:
                st.success("Inference: The concrete has **high workability**, suitable for sections with heavy reinforcement or complex formwork.")
            else:
                st.warning("Inference: The slump value entered is unusually high. Please check for input errors or very high fluidity mixes.")

    elif test_type == "Compaction Factor":
        cf_value = st.number_input("Enter Compaction Factor", min_value=0.0, max_value=1.0, step=0.01)
        if st.button("Analyze"):
            st.markdown(f"### Compaction Factor: **{cf_value:.2f}**")
            if cf_value < 0.75:
                st.success("Inference: The concrete has **very low workability** and would require intensive compaction. Suitable for dry mixes.")
            elif 0.75 <= cf_value < 0.85:
                st.success("Inference: The mix has **low workability** and is best used where mechanical vibration is provided during placing.")
            elif 0.85 <= cf_value < 0.95:
                st.success("Inference: The concrete has **medium workability**, generally workable with hand compaction.")
            elif cf_value >= 0.95:
                st.success("Inference: The concrete has **high workability**, ideal for heavily reinforced structures and areas with limited access.")

    elif test_type == "Flow Table":
        flow_percent = st.number_input("Enter Flow Value (%)", min_value=0.0, max_value=150.0, step=0.1)
        if st.button("Analyze"):
            st.markdown(f"### Flow Value: **{flow_percent:.1f}%**")
            if flow_percent < 25:
                st.success("Inference: The flow value indicates **very low workability**, suitable only where vibration is possible.")
            elif 25 <= flow_percent < 50:
                st.success("Inference: The mix has **low workability**, commonly used for precast sections with controlled compaction.")
            elif 50 <= flow_percent < 100:
                st.success("Inference: The concrete has **medium workability**, applicable for normal structural work.")
            elif flow_percent >= 100:
                st.success("Inference: The concrete shows **high workability**, beneficial in areas with congested reinforcement or complex molds.")

    elif test_type == "Vee Bee":
        vb_time = st.number_input("Enter Vee Bee Time (seconds)", min_value=0.0)
        if st.button("Analyze"):
            st.markdown(f"### Vee Bee Time: **{vb_time:.1f} seconds**")
            if vb_time > 10:
                st.success("Inference: The concrete has **very low workability**, typically seen in dry mixes used for pavements or roads.")
            elif 5 <= vb_time <= 10:
                st.success("Inference: The concrete has **low workability**, where mechanical vibration may be necessary for full compaction.")
            elif 2 <= vb_time < 5:
                st.success("Inference: The mix has **medium workability**, usable in reinforced concrete work with moderate reinforcement.")
            elif vb_time < 2:
                st.success("Inference: The concrete exhibits **high workability**, indicating a fluid mix that flows easily and requires little effort to compact.")

#------------------------------------bitumen analysis---------------------------
elif option == "Bitumen Analysis":
    st.markdown("""
    ### 🛠 Bitumen Analysis
    Select the test you conducted to analyze the properties of bitumen.
    """)

    test_conducted = st.selectbox(
        "Select Test Conducted",
        ("Ductility", "Stripping Value", "Softness Test", "Flash and Fire Point")
    )

    if test_conducted == "Ductility":
        breaking_length = st.number_input("Enter the Breaking Length (in cm):", min_value=0.0)

        if st.button("Analyze"):
            # Ductility Analysis based on IS Classification
            if breaking_length < 40:
                st.write("🔴 The bitumen is classified as **Low Ductility**. The bitumen has low flexibility and is prone to cracking under low temperatures.")
            elif 40 <= breaking_length <= 80:
                st.write("🟡 The bitumen is classified as **Medium Ductility**. This bitumen has moderate flexibility and performs well in moderate temperature conditions.")
            else:
                st.write("🟢 The bitumen is classified as **High Ductility**. It has high flexibility, making it suitable for low-temperature applications without cracking.")

    elif test_conducted == "Stripping Value":
        stripping_value = st.number_input("Enter Stripping Value (percentage):", min_value=0.0)

        if st.button("Analyze"):
            # Stripping Value Analysis
            if stripping_value < 0.5:
                st.write("🟢 The stripping value is within acceptable limits. The bitumen has good adhesion to aggregates.")
            elif 0.5 <= stripping_value <= 2.0:
                st.write("🟡 The stripping value is on the borderline. A slight increase in the stripping value can affect the durability of the mixture.")
            else:
                st.write("🔴 The stripping value is too high, indicating poor adhesion of bitumen to aggregates. This can lead to premature failure of the pavement.")

    elif test_conducted == "Softness Test":
        softness_value = st.number_input("Enter Softness Value (in °C):", min_value=0.0)

        if st.button("Analyze"):
            # Softness Test Analysis
            if softness_value < 40:
                st.write("🟢 The bitumen shows good resistance to softening at higher temperatures. It is suitable for high-temperature applications.")
            elif 40 <= softness_value <= 55:
                st.write("🟡 The bitumen has moderate resistance to softening. It can perform well in average temperature conditions.")
            else:
                st.write("🔴 The bitumen is prone to excessive softening at higher temperatures, which may cause deformation of the pavement.")

    elif test_conducted == "Flash and Fire Point":
        flash_point = st.number_input("Enter Flash Point (in °C):", min_value=0.0)
        fire_point = st.number_input("Enter Fire Point (in °C):", min_value=0.0)

        if st.button("Analyze"):
            # Flash and Fire Point Analysis
            if flash_point > 230 and fire_point > 250:
                st.write("🟢 The bitumen has a high flash and fire point, making it safe for high-temperature operations.")
            elif 180 <= flash_point <= 230 and 200 <= fire_point <= 250:
                st.write("🟡 The bitumen has moderate flash and fire points. It may not be suitable for extreme temperature conditions.")
            else:
                st.write("🔴 The bitumen has a low flash and fire point, posing a risk of fire hazard during handling.")

  
