from fastapi import Depends
from functools import lru_cache
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from db.postgres import get_session
from models.activities import Activity
from models.companies import Company
from schemas.companies import CompanySchema


class CompanyService:
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
            Company.building.longitude <= right,
            Company.building.longitude >= left,
            Company.building.latitude <= top,
            Company.building.latitude >= bot
        ]

    async def obj_conversion(self, obj: Company) -> CompanySchema:
        """Conversion obj to schema."""
        obj_dict = obj.__dict__
        return CompanySchema(**obj_dict)

    async def get(self, item_uuid: UUID) -> CompanySchema:
        query = select(Company).where(Company.uuid == item_uuid)
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
        activity_uuid: UUID = None,
        building_uuid: UUID = None,
        name: str = None,
        longitude: float = None,
        latitude: float = None,
        radius: int = None
    ) -> list[CompanySchema]:
        where_clauses = []
        if activity_uuid:
            where_clauses.append(
                or_(
                    Company.activities.any(Activity.uuid == activity_uuid),
                    Company.activities.any(
                        Activity.path.contains(activity_uuid.__str__()))
                )
            )
        if building_uuid:
            where_clauses.append(Company.building_uuid == building_uuid)
        if name:
            where_clauses.append(Company.name.ilike(f'%{name}%'))

        if radius:
            geo_filter = await self.calc_radius_filter(
                longitude, latitude, radius)
            where_clauses += geo_filter

        query = select(Company)
        if where_clauses:
            query = query.where(and_(*where_clauses))
        result = await self.session.execute(
            query.limit(limit).offset(offset))
        items = result.scalars().unique()
        items = [await self.obj_conversion(item) for item in items]
        return items


@lru_cache()
def get_company_service(
    session: AsyncSession = Depends(get_session)
) -> CompanyService:
    return CompanyService(
        session=session
    )
