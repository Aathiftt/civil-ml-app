import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.title("Civil Engineering ML Toolkit")

# Sidebar menu
option = st.sidebar.selectbox("Select Tool", ["Concrete Strength Predictor", "Soil Classification"])

# -------------------- Concrete Strength Predictor ------------------------
if option == "Concrete Strength Predictor":
    st.header("Concrete Strength Predictor")

    @st.cache_data
    def load_concrete_data():
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/compressive/Concrete_Data.xls"
        return pd.read_excel(url)

    data = load_concrete_data()
    X = data.drop("Concrete compressive strength(MPa, megapascals) ", axis=1)
    y = data["Concrete compressive strength(MPa, megapascals) "]
    model = LinearRegression()
    model.fit(X, y)

    # Inputs
    cement = st.number_input("Cement (kg/m³)", value=500.0)
    slag = st.number_input("Blast Furnace Slag (kg/m³)", value=0.0)
    fly_ash = st.number_input("Fly Ash (kg/m³)", value=0.0)
    water = st.number_input("Water (kg/m³)", value=200.0)
    superplasticizer = st.number_input("Superplasticizer (kg/m³)", value=0.0)
    coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", value=1000.0)
    fine_agg = st.number_input("Fine Aggregate (kg/m³)", value=700.0)
    age = st.number_input("Age (days)", value=28)

    input_data = np.array([[cement, slag, fly_ash, water, superplasticizer, coarse_agg, fine_agg, age]])
    strength = model.predict(input_data)[0]

    st.success(f"Predicted Compressive Strength: {strength:.2f} MPa")

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

    # User inputs
    ll = st.number_input("Liquid Limit (%)", value=40.0)
    pl = st.number_input("Plastic Limit (%)", value=25.0)

    result = clf.predict([[ll, pl]])
    predicted_label = label_encoder.inverse_transform(result)[0]

    st.success(f"Predicted Soil Type: {predicted_label}")
