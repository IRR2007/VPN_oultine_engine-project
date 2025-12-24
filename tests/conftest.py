import pytest_asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base
from database.handlerDB import DataBaseHandler


@pytest_asyncio.fixture
async def db_handler():
    db_url = (
        f"postgresql+asyncpg://"
        f"{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}"
        f"/{os.environ['DB_NAME']}"
    )

    engine = create_async_engine(db_url, echo=False)

    session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    handler = DataBaseHandler(session_maker, engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield handler

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
