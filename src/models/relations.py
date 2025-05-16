from sqlalchemy import ForeignKey, Table, Column

from db.postgres import Base


company_activity = Table(
    'company_activity',
    Base.metadata,
    Column('company_uuid', ForeignKey('companies.uuid'), primary_key=True),
    Column('activity_uuid', ForeignKey('activities.uuid'), primary_key=True),
)
