from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.postgres import Base
from models.relations import company_activity


class Activity(Base):
    __tablename__ = 'activities'

    name: Mapped[str] = mapped_column(String(200))
    path: Mapped[str] = mapped_column(String(110), default='/')

    companies = relationship(
        'Company',
        secondary=company_activity,
        back_populates='activities',
        # lazy='joined'
    )

    def __repr__(self) -> str:
        return f'<Activity {self.name}>'
