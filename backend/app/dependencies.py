from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connect import session_maker


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session =   session_maker.db_session()
    async with session:
        yield session
