from datetime import datetime
from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from sqlmodel import Session
from sqlalchemy.exc import NoResultFound


from ..database import get_session
from ..dto.requests.company_request import CreateCompanyRequest, UpdateCompanyRequest
from ..dto.response.base import BaseResponse
from ..utils.reponse_helper import response_helper
from ..repositories.company_repository import CompanyRepository
from ..models.company import Company

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


def get_company_repository(db: db_dependency) -> CompanyRepository:
    return CompanyRepository(db)


company_repository_dependency = Annotated[
    CompanyRepository, Depends(get_company_repository)
]


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[Company]]
)
async def get_all(
    company_repository: company_repository_dependency, offset: int = 0, limit: int = 100
):
    companies, total = company_repository.get_all(offset=offset, limit=limit)

    result = []
    for company in companies:
        result.append(Company.model_validate(company).model_dump(mode="json"))

    return response_helper(
        success=True,
        data={"companies": result, "total": total},
        message=f"Retrieved companies successfully",
    )


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[Company],
)
async def get_one_by_id(
    company_id: int, company_repository: company_repository_dependency
):
    try:
        company = company_repository.get_one_by(column_name="id", value=company_id)
        return response_helper(
            success=True,
            data={"company": Company.model_validate(company).model_dump(mode="json")},
            message="Company retrieved successfully",
        )
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Company not found",
            error=str(e),
        )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[Company]
)
async def create(
    request: CreateCompanyRequest, company_repository: company_repository_dependency
):
    try:
        company = company_repository.create(
            Company(**request.model_dump(), created_at=datetime.now())
        )
        return response_helper(
            success=True,
            data={"company": Company.model_validate(company).model_dump(mode="json")},
            message="Company created successfully",
        )
    except Exception as e:
        return response_helper(
            success=False,
            message="Failed to create company",
            error=str(e),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.put(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[Company],
)
async def update(
    company_id: int,
    request: UpdateCompanyRequest,
    company_repository: company_repository_dependency,
):
    try:
        company = company_repository.get_one_by("id", company_id)

        company.name = request.name if request.name is not None else company.name
        company.industry = (
            request.industry if request.industry is not None else company.industry
        )
        company.country = (
            request.country if request.country is not None else company.country
        )
        company.updated_at = datetime.now()

        result = company_repository.update(id=company_id, company=company)

        return response_helper(
            success=True,
            data={"company": Company.model_validate(result).model_dump(mode="json")},
            message="Company updated successfully",
        )
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Company not found",
            error=str(e),
        )


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(company_id: int, company_repository: company_repository_dependency):
    try:
        company = company_repository.get_one_by("id", company_id)
        company_repository.delete(company)
        return response_helper(success=True, message="Company deleted successfully")
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Company not found",
            error=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )
