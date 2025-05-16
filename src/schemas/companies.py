from schemas.base import MyBaseModelRepr
from schemas.activities import ActivitySchema
from schemas.buildings import BuildingSchema


class CompanySchema(MyBaseModelRepr):
    name: str
    phones: list[str]
    building: BuildingSchema
    activities: list[ActivitySchema]
