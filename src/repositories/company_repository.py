from sqlmodel import Session, select
from typing import Any
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func


from ..models.company import Company


class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, company: Company):
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_all(self, offset: int = 0, limit: int = 100):
        companies = self.db.exec(select(Company).offset(offset).limit(limit)).all()
        total = self.db.exec(select(func.count()).select_from(Company)).one()
        return companies, total

    def get_one_by(self, column_name: str, value: Any):
        company = self.db.exec(
            select(Company).where(getattr(Company, column_name) == value)
        ).first()
        if not company:
            raise NoResultFound(f"Company with {column_name}={value} not found")
        return company

    def update(self, id: int, company: Company):
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)

        return company

    def delete(self, company: Company):
        self.db.delete(company)
        self.db.commit()
