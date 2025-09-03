from sqlmodel import Session, select
from typing import Any
from sqlalchemy.exc import NoResultFound


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
        return self.db.exec(select(Company).offset(offset).limit(limit)).all()

    def get_one_by(self, column_name: str, value: Any):
        company = self.db.exec(
            select(Company).where(getattr(Company, column_name) == value)
        ).first()
        if not company:
            raise NoResultFound(f"Company with {column_name}={value} not found")
        return company

    def update(self, id: int, company: Company):
        # existCompany = self.get_one_by("id", id)

        # existCompany.name = company.name
        # existCompany.industry = company.industry
        # existCompany.country = company.country

        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)

        return company

    def delete(self, company: Company):
        self.db.delete(company)
        self.db.commit()
