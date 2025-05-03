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

    # Calculate the other indices
    st.subheader("Calculate Other Indices")
    st.markdown("Please input the values for Liquid Limit, Plastic Limit, Shrinkage Limit, and Natural Water Content to calculate the following indices:")

    liquid_limit_input = st.number_input("Enter Liquid Limit (%)", min_value=0.0)
    plastic_limit_input = st.number_input("Enter Plastic Limit (%)", min_value=0.0)
    shrinkage_limit_input = st.number_input("Enter Shrinkage Limit (%)", min_value=0.0)
    natural_water_content = st.number_input("Enter Natural Water Content (%)", min_value=0.0)

    if st.button("Calculate Other Indices"):
        try:
            # Plasticity Index (PI)
            pi = liquid_limit_input - plastic_limit_input

            # Flow Index (FI) - Using a sample 1 and sample 2 data
            # Assuming w1 and w2 values are provided or calculated
            fi = (w1 - w2) / math.log10(n2 / n1) if w1 is not None and w2 is not None else None

            # Toughness Index (TI)
            ti = pi / fi if fi != 0 else 0

            # Consistency Index (CI) - Assuming a sample water content 'w' is provided
            ci = (liquid_limit_input - natural_water_content) / pi if pi != 0 else 0

            # Shrinkage Index (SI)
            si = liquid_limit_input - shrinkage_limit_input

            st.success(f"Plasticity Index (PI) = {pi:.2f}")
            if fi is not None:
                st.success(f"Flow Index (FI) = {fi:.2f}")
            st.success(f"Toughness Index (TI) = {ti:.2f}")
            st.success(f"Consistency Index (CI) = {ci:.2f}")
            st.success(f"Shrinkage Index (SI) = {si:.2f}")
        except Exception as e:
            st.error(f"Error calculating indices: {str(e)}")
