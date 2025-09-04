from datetime import datetime
from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from sqlmodel import Session
from sqlalchemy.exc import NoResultFound


from ..database import get_session
from ..dto.requests.waste_request import CreateWasteRequest, UpdateWasteRequest
from ..dto.response.base import BaseResponse
from ..utils.reponse_helper import response_helper
from ..repositories.waste_repository import WasteRepository
from ..models.waste import Waste
from .company import company_repository_dependency

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


def get_waste_repository(db: db_dependency) -> WasteRepository:
    return WasteRepository(db)


waste_repository_dependency = Annotated[WasteRepository, Depends(get_waste_repository)]


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=BaseResponse[List[Waste]]
)
async def get_all(
    waste_repository: waste_repository_dependency, offset: int = 1, limit: int = 100
):
    wastes, total = waste_repository.get_all(offset=offset, limit=limit)

    result = []
    for waste in wastes:
        result.append(Waste.model_validate(waste).model_dump(mode="json"))

    return response_helper(
        success=True,
        data={"wastes": result, "total": total},
        message=f"Retrieved wastes successfully",
    )


@router.get(
    "/{waste_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[Waste],
)
async def get_one_by_id(waste_id: int, waste_repository: waste_repository_dependency):
    try:
        waste = waste_repository.get_one_by(column_name="id", value=waste_id)
        return response_helper(
            success=True,
            data={"waste": Waste.model_validate(waste).model_dump(mode="json")},
            message="Waste retrieved successfully",
        )
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Waste not found",
            error=str(e),
        )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[Waste]
)
async def create(
    request: CreateWasteRequest,
    waste_repository: waste_repository_dependency,
    company_repository: company_repository_dependency,
):
    try:
        company_repository.get_one_by("id", request.company_id)

        waste = waste_repository.create(
            Waste(**request.model_dump(), created_at=datetime.now())
        )
        return response_helper(
            success=True,
            data={"waste": Waste.model_validate(waste).model_dump(mode="json")},
            message="Waste created successfully",
        )
    except Exception as e:
        return response_helper(
            success=False,
            message="Failed to create waste",
            error=str(e),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.put(
    "/{waste_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse[Waste],
)
async def update(
    waste_id: int,
    request: UpdateWasteRequest,
    waste_repository: waste_repository_dependency,
    company_repository: company_repository_dependency,
):
    try:
        company_repository.get_one_by("id", request.company_id)

        waste = waste_repository.get_one_by("id", waste_id)

        waste.date = request.date if request.date is not None else waste.date
        waste.type = request.type if request.type is not None else waste.type
        waste.weight = request.weight if request.weight is not None else waste.weight
        waste.location = (
            request.location if request.location is not None else waste.location
        )
        waste.company_id = (
            request.company_id if request.company_id is not None else waste.company_id
        )
        waste.updated_at = datetime.now()

        result = waste_repository.update(id=waste_id, waste=waste)

        return response_helper(
            success=True,
            data={"waste": Waste.model_validate(result).model_dump(mode="json")},
            message="Waste updated successfully",
        )
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Waste not found",
            error=str(e),
        )


@router.delete("/{waste_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(waste_id: int, waste_repository: waste_repository_dependency):
    try:
        waste = waste_repository.get_one_by("id", waste_id)
        waste_repository.delete(waste)
        return response_helper(success=True, message="Waste deleted successfully")
    except NoResultFound as e:
        return response_helper(
            success=False,
            message="Waste not found",
            error=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )
