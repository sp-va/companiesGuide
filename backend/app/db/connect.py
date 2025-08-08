import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

class SessionMaker:
    def __init__(self) -> None:
        self._engine = create_async_engine(
            url=f"postgresql+asyncpg://{os.getenv("POSTGRES_PASSWORD", "postgres")}:{os.getenv("POSTGRES_USER", "postgres")}@db:5432/{os.getenv("POSTGRES_DB", "postgres")}"
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory


session_maker = SessionMaker()
