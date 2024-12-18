# Main Streamlit application

import streamlit as st
import requests

st.title("Landscaping Cost Estimator")

time_spent = st.number_input("Time Spent (hours)", min_value=0.0)
labor_cost_per_hour = st.number_input("Labor Cost per Hour", min_value=0.0)
gas_expenses = st.number_input("Gas Expenses", min_value=0.0)
additional_charges = st.number_input("Additional Charges", min_value=0.0)

if st.button("Calculate"):
    payload = {
        "time_spent": time_spent,
        "labor_cost_per_hour": labor_cost_per_hour,
        "gas_expenses": gas_expenses,
        "additional_charges": additional_charges
    }
    response = requests.post("http://127.0.0.1:8000/calculate", json=payload)
    if response.status_code == 200:
        st.write("Total Cost:", response.json()["total_cost"])
        st.write("Breakdown:", response.json()["breakdown"])
