from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .waste import Waste


class Company(BaseModel, table=True):
    __tablename__ = "companies"  # type: ignore

    name: str = Field(description="name of the company")
    industry: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)

    # Relationships
    wastes: Optional[List["Waste"]] = Relationship(back_populates="company")
