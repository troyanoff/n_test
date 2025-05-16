# from __future__ import annotations
from sqlalchemy import (
    ForeignKey, String, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.postgres import Base
from models.relations import company_activity


class Company(Base):
    __tablename__ = 'companies'

    name: Mapped[str] = mapped_column(String(200))
    phones: Mapped[list[str]] = mapped_column(ARRAY(String(15)))

    building_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('buildings.uuid', ondelete='SET NULL')
    )
    building: Mapped[Base] = relationship(
        'Building',
        back_populates='companies',
        lazy='joined'
    )

    activities = relationship(
        'Activity',
        secondary=company_activity,
        back_populates='companies',
        lazy='joined'
    )

    def __repr__(self) -> str:
        return f'<Company {self.name}>'
