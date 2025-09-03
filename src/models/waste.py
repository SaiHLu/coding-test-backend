from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .company import Company


class Waste(BaseModel, table=True):
    __tablename__ = "wastes"  # type: ignore

    date: datetime = Field(default_factory=datetime.now)
    type: Optional[str] = Field(default=None)
    weight: Optional[float] = Field(default=None, description="Weight in kilograms")
    location: Optional[str] = Field(default=None)
    company_id: Optional[int] = Field(default=None, foreign_key="companies.id")

    # Relationships
    company: Optional["Company"] = Relationship(back_populates="wastes")
