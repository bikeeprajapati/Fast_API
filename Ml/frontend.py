import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter the details below to predict your insurance premium category.")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=499.0, value=70.0)
height = st.number_input("Height (cm)", min_value=1.0, max_value=299.0, value=170.0)
income_lpa = st.number_input("Income (LPA)", min_value=1.0, max_value=999.0, value=10.0)
smoker = st.selectbox("Smoker", options=["yes", "no"])

# Match backend expectation: tier_1, tier_2, tier_3
city = st.selectbox("City Tier", options=["tier_1", "tier_2", "tier_3"])

occupation = st.selectbox("Occupation", options=[
    "retired", "freelancer", "student", "government_job",
    "business_owner", "unemployed", "private_job"
])

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            prediction = response.json().get("predicted_insurance_premium_category")
            st.success(f"Predicted Insurance Premium Category: {prediction}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError as e:
        st.error(f"API request failed: {e}")
