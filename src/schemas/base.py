import orjson

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class MyBaseModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True


class MyBaseModelRepr(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        populate_by_name = True
