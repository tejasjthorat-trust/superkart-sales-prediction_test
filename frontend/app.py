import streamlit as st
import pandas as pd
import requests
BACKEND_URL = "http://backend:7860"
st.title("SuperKart System")
# Sidebar for user input
st.sidebar.header("Input Features")

# Define input fields for a single prediction
product_weight = st.sidebar.number_input("Product Weight", min_value=1.0, max_value=30.0, value=12.66)
product_sugar_content = st.sidebar.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
product_allocated_area = st.sidebar.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027)
product_mrp = st.sidebar.number_input("Product MRP", min_value=1.0, max_value=300.0, value=117.08)
store_size = st.sidebar.selectbox("Store Size", ['Medium', 'High', 'Small'])
store_location_city_type = st.sidebar.selectbox("Store Location City Type", ['Tier 2', 'Tier 1', 'Tier 3'])
store_type = st.sidebar.selectbox("Store Type", ['Supermarket Type2', 'Grocery Store', 'Supermarket Type1', 'Departmental Store'])
product_id_char = st.sidebar.selectbox("Product ID Character", ['FD', 'DR', 'NC'])
store_age_years = st.sidebar.number_input("Store Age (Years)", min_value=0, max_value=100, value=16)
product_type_category = st.sidebar.selectbox("Product Type Category", ['Non Perishables', 'Perishables'])

# Create a dictionary for the single prediction payload
single_prediction_payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Product_Id_char": product_id_char,
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": product_type_category
}

# Button for single prediction
if st.sidebar.button("Predict Single Item Sales"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=single_prediction_payload)
        if response.status_code == 200:
            prediction = response.json().get('Sales')
            st.success(f"Predicted Sales for Single Item: ${prediction:,.2f}")
        else:
            st.error(f"Error making single prediction: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please ensure the backend is running.")

# File uploader for batch predictions
st.sidebar.subheader("Batch Prediction")
uploaded_file = st.sidebar.file_uploader("Upload CSV for Batch Prediction", type=["csv"])

if uploaded_file is not None:
    if st.sidebar.button("Predict Batch Sales"):
        try:
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)

            if response.status_code == 200:
                predictions = response.json()
                st.write("Batch Predictions:")
                st.json(predictions)
            else:
                st.error(f"Error making batch prediction: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Please ensure the backend is running.")
