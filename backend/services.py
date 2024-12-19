# Cost calculation and PDF generation logic

import pandas as pd
from fpdf import FPDF
from datetime import datetime

def calculate_costs(data):
    # Ensure data contains all necessary keys
    workers = data.get('workers', 0)
    labor_cost_per_hour = data['labor_cost']
    labor_cost = labor_cost_per_hour * data['time_spent'] * workers
    
    # Safely get 'equipment_wear' and set a default of 0 if not present
    equipment_wear = data.get('equipment_wear', 0.0)  # Default to 0 if not present
    
    total_cost = labor_cost + data['gas_expenses'] + equipment_wear + data['additional_charges']
    
    # Breakdown
    breakdown = {
        "Labor": labor_cost,
        "Gas": data['gas_expenses'],
        "Equipment Wear/Tear": equipment_wear,  # Add the equipment wear/tear to breakdown
        "Additional Charges": data['additional_charges']
    }
    
    return total_cost, breakdown

# Generate a modern, professional-looking invoice
def generate_invoice(data, breakdown, total_cost, file_name="invoice.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Set font for the title and make it bold and larger size
    pdf.set_font("Helvetica", style='B', size=16)
    pdf.cell(200, 10, txt="Raul's Lawn & Garden Invoice", ln=True, align='C')
    
    # Set font for the date and make it smaller size
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, txt=f"Date: {data.get('date', datetime.now().strftime('%Y-%m-%d'))}", ln=True, align='C')

    # Add a line to separate the title and body
    pdf.ln(10)
    
    # Set font for the breakdown heading and make it bold
    pdf.set_font("Helvetica", style='B', size=12)
    pdf.cell(200, 10, txt="Cost Breakdown", ln=True, align='L')

    # Set font for the breakdown values and make it regular
    pdf.set_font("Helvetica", size=12)
    for key, value in breakdown.items():
        # Use a two-column layout with the item name on the left and the cost on the right
        pdf.cell(100, 10, txt=f"{key}:", border=0, align='L')
        pdf.cell(90, 10, txt=f"${value:.2f}", border=0, align='R')
        pdf.ln(6)  # Line break after each item

    # Add a line to separate the breakdown and total cost
    pdf.ln(6)

    # Set font for the total cost (bold and larger size)
    pdf.set_font("Helvetica", style='B', size=12)
    pdf.cell(100, 10, txt="Total Cost:", border=0, align='L')
    pdf.cell(90, 10, txt=f"${total_cost:.2f}", border=0, align='R')
    
    # Add space before the footer (if needed)
    pdf.ln(15)
    
    # Add footer (optional, you can customize it further)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(200, 10, txt="Thank you for choosing Raul's Lawn & Garden!", ln=True, align='C')
    
    # Output the PDF to a file
    pdf.output(file_name)
    return file_name
