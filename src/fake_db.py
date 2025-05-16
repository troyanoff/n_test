import asyncio
import random
import uuid

from faker import Faker
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)

from db.postgres import dsn
from models.activities import Activity
from models.buildings import Building
from models.companies import Company
from models.relations import company_activity


fake = Faker('ru_RU')


async def create_company_relations(session: AsyncSession):
    buildings = []

    for _ in range(1000):
        integer = random.randint(-179, 179)
        fraction = random.randint(0, 999999)
        long = float(f'{integer}.{fraction:06d}')

        integer = random.randint(-89, 89)
        fraction = random.randint(0, 999999)
        lat = float(f'{integer}.{fraction:06d}')

        buildings.append(
            Building(
                address=fake.text(100),
                longitude=long,
                latitude=lat
            )
        )

    session.add_all(buildings)
    await session.commit()

    companies = []
    for _ in range(100):
        phones = []
        for _ in range(random.randint(1, 5)):
            one = random.randint(1, 9)
            two = random.randint(10, 99)
            three = random.randint(100, 999)
            phones.append(f'{one}-{three}-{three}-{two}-{two}')
        companies.append(
            Company(
                name=fake.text(100),
                phones=phones,
                building_uuid=random.choice(buildings).uuid
            )
        )

    session.add_all(companies)
    await session.commit()

    last_activities = []
    activities = []
    for _ in range(5):
        one_uuid = uuid.uuid4()
        activities.append(
            Activity(
                uuid=one_uuid,
                name=fake.text(15),
                path=f'{one_uuid}'
            )
        )
        for _ in range(15):
            two_uuid = uuid.uuid4()
            activities.append(
                Activity(
                    uuid=one_uuid,
                    name=fake.text(15),
                    path=f'{one_uuid}/{two_uuid}'
                )
            )
            for _ in range(50):
                three_uuid = uuid.uuid4()
                last_act = Activity(
                    uuid=one_uuid,
                    name=fake.text(15),
                    path=f'{one_uuid}/{two_uuid}/{three_uuid}'
                )
                activities.append(last_act)
                last_activities.append(last_activities)

    session.add_all(activities)
    await session.commit()

    values_relation = []
    for company in companies:
        acts = random.sample(last_activities, k=random.randint(2, 4))
        for activity in acts:
            values_relation.append(
                {'company_uuid': company.uuid, 'activity_uuid': activity.uuid}
            )

    stmt = insert(company_activity).values(values_relation)
    await session.execute(stmt)
    await session.commit()


async def async_main() -> None:
    engine = create_async_engine(dsn)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        await create_company_relations(session)

    await engine.dispose()


asyncio.run(async_main())
