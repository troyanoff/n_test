from sqlalchemy import (
    String, DECIMAL, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from db.postgres import Base


class Building(Base):

    address: Mapped[str] = mapped_column(String(512))
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    latitude: Mapped[float] = mapped_column(DECIMAL(8, 6))

    companies = relationship(
        'Company',
        back_populates='building',
        # lazy='joined'
    )

    __table_args__ = (
        CheckConstraint(
            'longitude >= -180 AND longitude <= 180',
            name='check_longitude_range'
        ),
        CheckConstraint(
            'latitude >= -90 AND latitude <= 90',
            name='check_latitude_range'
        ),
    )

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not -180 <= value <= 180:
            raise ValueError('longitude must be between -180 and 180')
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not -90 <= value <= 90:
            raise ValueError('latitude must be between -90 and 90')
        return value

    def __repr__(self) -> str:
        return f'<Building {self.address}>'
