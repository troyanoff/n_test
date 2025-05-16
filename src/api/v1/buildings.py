from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus

from services.buildings import get_building_service, BuildingService
from schemas.buildings import BuildingSchema


router = APIRouter()


@router.get(
    '/',
    response_model=list[BuildingSchema],
    response_model_by_alias=False,
    summary='Get list',
    description='Get building list'
)
async def get_list(
    radius: int = Query(None, ge=0, le=180),
    longitude: int = Query(None, ge=-180, le=180),
    latitude: int = Query(None, ge=-90, le=90),
    limit: int = 20,
    offset: int = 0,
    service: BuildingService = Depends(get_building_service)
) -> list[BuildingSchema]:
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
        longitude=longitude,
        latitude=latitude,
        radius=radius
    )
    return items
