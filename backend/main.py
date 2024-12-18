# FastAPI entry point

from fastapi import FastAPI, HTTPException
from models import JobInput, JobOutput
from services import calculate_costs, generate_invoice
from database import save_job

app = FastAPI()

# Calculates 
@app.post("/calculate", response_model=JobOutput)
def calculate_job(input_data: JobInput):
    # Perform cost calculations
    total_cost, breakdown = calculate_costs(input_data.model_dump())
    return {"total_cost": total_cost, "breakdown": breakdown}

@app.post("/generate-invoice")
def create_invoice(input_data: JobInput):
    # Perform cost calculations
    total_cost, breakdown = calculate_costs(input_data.model_dump())

    # Generate the invoice
    file_name = generate_invoice(input_data.model_dump(), breakdown, total_cost)

    return {"message": "Invoice generated", "file_name": file_name}

@app.post("/save-job")
def save_job_data(input_data: JobInput):
    # Perform cost calculations
    total_cost, breakdown = calculate_costs(input_data.model_dump())

    # Save to database
    save_job({
        "date": input_data.date or "N/A",
        "time_spent": input_data.time_spent,
        "labor_cost": input_data.time_spent * input_data.labor_cost_per_hour,
        "gas_expenses": input_data.gas_expenses,
        "additional_charges": input_data.additional_charges,
        "total_cost": total_cost
    })

    return {"message": "Job data saved successfully"}
