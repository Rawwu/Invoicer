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

        submit_button = st.form_submit_button("Calculate")

    if submit_button:
        # Validate inputs
        if time_spent > 0 and labor_cost > 0:
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
                    st.session_state.job_data["breakdown"] = result["breakdown"]
                    st.session_state.job_data["total_cost"] = result["total_cost"]

                    # Display results
                    st.subheader("Cost Breakdown")
                    st.write(f"**Total Cost:** ${result['total_cost']:.2f}")
                    st.write("**Breakdown:**")
                    for key, value in result["breakdown"].items():
                        st.write(f"{key}: ${value:.2f}")

                    # Visualization
                    st.subheader("Visualization")
                    df = pd.DataFrame(list(result["breakdown"].items()), columns=["Category", "Cost"])
                    fig, ax = plt.subplots()
                    df.plot(kind="bar", x="Category", y="Cost", ax=ax, legend=False)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")
        else:
            st.error("Please fill in all required fields.")

    # Generate Invoice
    if st.session_state.job_data:
        st.subheader("Generate Invoice")
        name = st.text_input("Job Name")
        date = st.date_input("Job Date")
        if st.button("Generate Invoice"):
            st.session_state.job_data["name"] = name
            st.session_state.job_data["date"] = str(date)

            try:
                invoice_response = requests.post(f"{API_URL}/generate-invoice", json=st.session_state.job_data)
                if invoice_response.status_code == 200:
                    st.download_button(
                        label="Download Invoice",
                        data=invoice_response.content,
                        file_name=f"invoice_{name}.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.error(f"Error generating invoice: {invoice_response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")

    # Save Job Logic
    if st.session_state.job_data:
        st.subheader("Save Job")
        name = st.text_input("Job Name for Save", key="save_name")
        date = st.date_input("Job Date for Save", key="save_date")
        if st.button("Save Job"):
            st.session_state.job_data["name"] = name
            st.session_state.job_data["date"] = str(date)
            try:
                save_response = requests.post(f"{API_URL}/save-job", json=st.session_state.job_data)
                if save_response.status_code == 200:
                    st.success("Job saved successfully!")
                else:
                    st.error(f"Error saving job: {save_response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")

elif option == "Saved Jobs":
    st.header("Saved Job Records")

    # Fetch saved jobs from backend
    try:
        response = requests.get(f"{API_URL}/saved-jobs")
        if response.status_code == 200:
            jobs = response.json()
            if jobs:

                # Convert jobs to DataFrame
                try:
                    df = pd.DataFrame(jobs)

                    # Ensure required columns exist
                    required_columns = [
                        "name",
                        "date",
                        "time_spent",
                        "labor_cost",
                        "gas_expenses",
                        "additional_charges",
                        "total_cost",
                    ]
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        st.error(f"Missing expected columns: {missing_columns}")
                    else:
                        # Format and rename columns
                        df = df[required_columns]
                        df.rename(
                            columns={
                                "name": "Name",
                                "date": "Date",
                                "time_spent": "Time Spent (hours)",
                                "labor_cost": "Labor Cost ($/hr)",
                                "gas_expenses": "Gas Expenses ($)",
                                "additional_charges": "Additional Charges ($)",
                                "total_cost": "Total Cost ($)",
                            },
                            inplace=True,
                        )

                        # Format numeric values
                        numeric_cols = [
                            "Time Spent (hours)",
                            "Labor Cost ($/hr)",
                            "Gas Expenses ($)",
                            "Additional Charges ($)",
                            "Total Cost ($)",
                        ]
                        df[numeric_cols] = df[numeric_cols].astype(float).round(2)

                        # Display table without the index
                        st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)
                except Exception as df_error:
                    st.error(f"Error processing jobs data: {df_error}")
            else:
                st.write("No jobs saved yet.")

        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")