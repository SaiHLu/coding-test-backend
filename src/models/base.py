from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
