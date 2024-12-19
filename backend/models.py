# Defines data models

from pydantic import BaseModel, Field
from typing import Optional

# Input model for job details
class JobInput(BaseModel):
    time_spent: float = Field(..., gt=0, description="Time spent in hours")
    labor_cost_per_hour: float = Field(..., gt=0, description="Labor cost per hour")
    gas_expenses: float = Field(..., ge=0, description="Gas expenses")
    additional_charges: float = Field(..., ge=0, description="Additional charges")
    name: Optional[str] = Field(None, description="Name of the job (optional)")
    date: Optional[str] = Field(None, description="Date of the job (optional)")

# Output model for calculations
class JobOutput(BaseModel):
    total_cost: float
    breakdown: dict
