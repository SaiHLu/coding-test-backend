from pydantic import BaseModel, Field
from typing import Optional


class CreateCompanyRequest(BaseModel):
    name: str = Field(
        description="Company name", min_length=2, examples=["Tech Innovators Inc."]
    )
    industry: str = Field(
        description="Industry sector", min_length=2, examples=["Software Development"]
    )
    country: str = Field(
        description="Country of operation", min_length=2, examples=["USA"]
    )


class UpdateCompanyRequest(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Company name",
        examples=["Tech Innovators Inc."],
    )
    industry: Optional[str] = Field(
        default=None,
        description="Industry sector",
        examples=["Software Development"],
    )
    country: Optional[str] = Field(
        default=None,
        description="Country of operation",
        examples=["USA"],
    )
