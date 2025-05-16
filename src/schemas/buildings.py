from schemas.base import MyBaseModelRepr


class BuildingSchema(MyBaseModelRepr):
    address: str
    longitude: float
    latitude: float
