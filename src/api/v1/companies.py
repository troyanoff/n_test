from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from uuid import UUID

from services.companies import get_company_service, CompanyService
from schemas.companies import CompanySchema


router = APIRouter()


@router.get(
    '/{item_uuid}',
    response_model=CompanySchema,
    response_model_by_alias=False,
    summary='Get',
    description='Get company'
)
async def get(
    item_uuid: UUID,
    service: CompanyService = Depends(get_company_service)
) -> CompanySchema:
    """Get item by uuid."""
    item = await service.get(item_uuid=item_uuid)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item not found',
        )
    return item


@router.get(
    '/',
    response_model=list[CompanySchema],
    response_model_by_alias=False,
    summary='Get list',
    description='Get company list'
)
async def get_list(
    activity_uuid: UUID = None,
    building_uuid: UUID = None,
    name: str = None,
    radius: int = Query(None, ge=0, le=180),
    longitude: float | int = Query(None, ge=-180, le=180),
    latitude: int | int = Query(None, ge=-90, le=90),
    limit: int = 20,
    offset: int = 0,
    service: CompanyService = Depends(get_company_service)
) -> list[CompanySchema]:
    """Get item list."""
    if ((radius or longitude or latitude)
            and (not radius or not longitude or not latitude)):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='radius, longitude and latitude must be indicated together',
        )

    items = await service.get_list(
        limit=limit,
        offset=offset,
        activity_uuid=activity_uuid,
        building_uuid=building_uuid,
        name=name,
        longitude=longitude,
        latitude=latitude,
        radius=radius
    )
    return items
