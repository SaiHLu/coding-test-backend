from sqlmodel import Session, func, select
from typing import Any
from sqlalchemy.exc import NoResultFound


from ..models.waste import Waste


class WasteRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, waste: Waste):
        self.db.add(waste)
        self.db.commit()
        self.db.refresh(waste)
        return waste

    def get_all(self, offset: int = 0, limit: int = 100):
        wastes = self.db.exec(select(Waste).offset(offset).limit(limit)).all()
        total = self.db.exec(select(func.count()).select_from(Waste)).one()
        return wastes, total

    def get_one_by(self, column_name: str, value: Any):
        waste = self.db.exec(
            select(Waste).where(getattr(Waste, column_name) == value)
        ).first()
        if not waste:
            raise NoResultFound(f"Waste with {column_name}={value} not found")
        return waste

    def update(self, id: int, waste: Waste):
        self.db.add(waste)
        self.db.commit()
        self.db.refresh(waste)

        return waste

    def delete(self, waste: Waste):
        self.db.delete(waste)
        self.db.commit()
