from sqlalchemy import delete, update, select, desc, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building
from app.models.organization import Organization

async def list_buildings(db: AsyncSession):
    ...

async def list_orgs_in_building(
        building_id: int,
        db: AsyncSession
):
    stmt = select(Organization).where(Organization.building_id == building_id)

    result = (await db.execute(stmt)).scalars().all()

    return result
