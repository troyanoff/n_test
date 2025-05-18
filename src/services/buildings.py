from fastapi import Depends
from functools import lru_cache
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from db.postgres import get_session
from models.buildings import Building
from schemas.buildings import BuildingSchema


class BuildingService:
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session: AsyncSession = session

    async def calc_radius_filter(
        self, long: float, lat: float, radius: int
    ) -> list:
        left = long - radius
        right = long + radius
        top = lat + radius
        bot = lat - radius
        if left < -180:
            left += 360
        if right > 180:
            right -= 360
        if top > 90:
            top = 90
        if bot < -90:
            bot = -90
        return [
            Building.longitude <= right,
            Building.longitude >= left,
            Building.latitude <= top,
            Building.latitude >= bot
        ]

    async def obj_conversion(self, obj: Building) -> BuildingSchema:
        """Conversion obj to schema."""
        return BuildingSchema.model_validate(obj, from_attributes=True)

    async def get(self, item_uuid: UUID) -> BuildingSchema:
        query = select(Building).where(Building.uuid == item_uuid)
        result = await self.session.execute(query)
        item = result.scalars().first()
        if not item:
            return None
        item = await self.obj_conversion(item)
        return item

    async def get_list(
        self,
        limit: int,
        offset: int,
        longitude: float = None,
        latitude: float = None,
        radius: int = None
    ) -> list[BuildingSchema]:
        where_clauses = []

        if radius:
            geo_filter = await self.calc_radius_filter(
                longitude, latitude, radius)
            where_clauses += geo_filter

        query = select(Building)
        if where_clauses:
            query = query.where(and_(*where_clauses))
        result = await self.session.execute(
            query.limit(limit).offset(offset))
        items = result.scalars().unique()
        items = [await self.obj_conversion(item) for item in items]
        return items


@lru_cache()
def get_building_service(
    session: AsyncSession = Depends(get_session)
) -> BuildingService:
    return BuildingService(
        session=session
    )
