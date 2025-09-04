from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateWasteRequest(BaseModel):
    date: datetime = Field(
        description="Date of waste collection", examples=["2025-09-03T10:00:00"]
    )
    type: str = Field(
        description="Type of waste", min_length=2, examples=["Plastic", "Organic"]
    )
    weight: float = Field(description="Weight in kilograms", gt=0, examples=[10.5])
    location: str = Field(
        description="Location where waste was collected",
        min_length=2,
        examples=["Warehouse A"],
    )
    company_id: int = Field(
        description="ID of the company that produced the waste", examples=[1]
    )


class UpdateWasteRequest(BaseModel):
    date: Optional[datetime] = Field(
        default=None,
        description="Date of waste collection",
        examples=["2025-09-03T10:00:00"],
    )
    type: Optional[str] = Field(
        default=None,
        description="Type of waste",
        examples=["Plastic", "Organic"],
    )
    weight: Optional[float] = Field(
        default=None,
        description="Weight in kilograms",
        gt=0,
        examples=[10.5],
    )
    location: Optional[str] = Field(
        default=None,
        description="Location where waste was collected",
        examples=["Warehouse A"],
    )
    company_id: Optional[int] = Field(
        default=None,
        description="ID of the company that produced the waste",
        examples=[1],
    )
