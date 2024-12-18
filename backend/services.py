# Cost calculation and PDF generation logic

import pandas as pd
from fpdf import FPDF
from datetime import datetime

def calculate_costs(data):
    labor_cost = data['time_spent'] * data['labor_cost_per_hour']
    total_cost = labor_cost + data['gas_expenses'] + data['additional_charges']
    breakdown = {
        "Labor": labor_cost,
        "Gas": data['gas_expenses'],
        "Additional Charges": data['additional_charges']
    }
    return total_cost, breakdown

# Generate an itemized invoice
def generate_invoice(data, breakdown, total_cost, file_name="invoice.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Landscaping Job Invoice", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Date: {data.get('date', datetime.now().strftime('%Y-%m-%d'))}", ln=True, align='L')

    pdf.cell(200, 10, txt="Breakdown:", ln=True, align='L')
    for key, value in breakdown.items():
        pdf.cell(200, 10, txt=f"{key}: ${value}", ln=True, align='L')

    pdf.cell(200, 10, txt=f"Total Cost: ${total_cost}", ln=True, align='L')

    pdf.output(file_name)
    return file_name
