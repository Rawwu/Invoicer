# FastAPI entry point

from fastapi import FastAPI, HTTPException
from models import JobInput, JobOutput
from services import calculate_costs, generate_invoice
from database import save_job, get_all_jobs
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

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

    return FileResponse(file_name, media_type='application/pdf', filename="invoice.pdf")

@app.post("/save-job")
def save_job_data(input_data: JobInput):
    # Perform cost calculations
    total_cost, breakdown = calculate_costs(input_data.model_dump())

    # Save to database
    save_job({
        "name": input_data.name,
        "date": input_data.date or "N/A",
        "time_spent": input_data.time_spent,
        "labor_cost": input_data.labor_cost,  # Align with frontend naming
        "gas_expenses": input_data.gas_expenses,
        "additional_charges": input_data.additional_charges,
        "total_cost": total_cost
    })

    return {"message": "Job data saved successfully"}

@app.get("/saved-jobs")
def get_saved_jobs():
    try:
        jobs = get_all_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch jobs")