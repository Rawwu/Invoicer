import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Title
st.title("Raul's Lawn & Garden Invoicer")

# Sidebar
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose a page:", ["Pricing Calculator", "Saved Jobs"])

# Initialize session state for job_data if it doesn't exist
if "job_data" not in st.session_state:
    st.session_state.job_data = None

# Job Cost Estimator Page
if option == "Pricing Calculator":
    st.header("Calculate Job Cost")

    # Form for job details
    with st.form("job_form"):
        time_spent = st.number_input("Time spent (hours):", min_value=0.0, step=0.1)
        labor_cost = st.number_input("Labor cost per hour ($):", min_value=0.0, step=0.1)
        gas_expenses = st.number_input("Gas expenses ($):", min_value=0.0, step=0.1)
        equipment_wear = st.number_input("Equipment wear/tear cost ($):", min_value=0.0, step=0.1)
        additional_charges = st.number_input("Additional charges ($):", min_value=0.0, step=0.1)

        # Buttons
        submit_button = st.form_submit_button("Calculate")
        save_button = st.form_submit_button("Save Job")

    if submit_button:
        # Prepare data for API
        st.session_state.job_data = {
            "time_spent": time_spent,
            "labor_cost_per_hour": labor_cost,
            "gas_expenses": gas_expenses,
            "equipment_wear": equipment_wear,
            "additional_charges": additional_charges,
        }

        # Send POST request to backend
        try:
            response = requests.post(f"{API_URL}/calculate", json=st.session_state.job_data)
            if response.status_code == 200:
                result = response.json()

                # Display results
                st.subheader("Cost Breakdown")
                st.write(f"**Total Cost:** ${result['total_cost']:.2f}")
                st.write("**Breakdown:**")
                for key, value in result['breakdown'].items():
                    st.write(f"{key}: ${value:.2f}")

                # Visualization
                st.subheader("Visualization")
                df = pd.DataFrame(list(result["breakdown"].items()), columns=["Category", "Cost"])
                fig, ax = plt.subplots()
                df.plot(kind="bar", x="Category", y="Cost", ax=ax, legend=False)
                plt.xticks(rotation=45)
                st.pyplot(fig)

                # Download Invoice Button
                st.download_button(
                    label="Download Invoice",
                    data=requests.post(f"{API_URL}/generate-invoice", json=st.session_state.job_data).content,
                    file_name="invoice.pdf",
                    mime="application/pdf",
                )

            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Failed to connect to the API: {e}")

    if save_button:
        if st.session_state.job_data:
            try:
                save_response = requests.post(f"{API_URL}/save-job", json=st.session_state.job_data)
                if save_response.status_code == 200:
                    st.success("Job saved successfully!")
                else:
                    st.error(f"Error saving job: {save_response.json()['detail']}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")
        else:
            st.warning("Please calculate the job first before saving it.")

# Saved Jobs Page
elif option == "Saved Jobs":
    st.header("Saved Job Records")

    # Fetch saved jobs from backend
    try:
        response = requests.get(f"{API_URL}/saved-jobs")
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                st.table(jobs)
            else:
                st.write("No jobs saved yet.")
        else:
            st.error(f"Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")
