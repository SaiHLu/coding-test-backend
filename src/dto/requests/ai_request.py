from pydantic import BaseModel, Field, field_validator


class AIRequest(BaseModel):
    input_type: str = Field(
        ..., description="Type of data to generate: 'company' or 'waste'"
    )

    @field_validator("input_type")
    @classmethod
    def validate_input_type(cls, v):
        if v not in ["company", "waste"]:
            raise ValueError("input_type must be either 'company' or 'waste'")
        return v
