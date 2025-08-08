import typing as t

from sqlalchemy import delete, update, select, desc, distinct, join, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from geoalchemy2 import Geometry

from app.models.building import Building
from app.models.organization import Organization, OrganizationsToActivities, PhoneNumber
from app.models.activity_type import Activity
from app.services.activities import get_activity_and_children_ids


async def list_orgs_of_exact_activity(
        activity_id: int,
        db: AsyncSession
):
    stmt = select(Organization).join(Organization.activity_types).where(Activity.id == activity_id).options(selectinload(Organization.activity_types))
    result = (await db.execute(stmt)).scalars().all()
    return result


async def get_org_full_info(
        org_id: int,
        db: AsyncSession
):
    # raw_sql = """SELECT organizations.id, organizations.title, activities.name, phone_numbers.number, buildings.address
    # FROM organizations
    # JOIN buildings
    # ON buildings.id = organizations.building_id

    # JOIN phone_numbers
    # ON organizations.id = phone_numbers.related_org

    # JOIN orgs_to_activities ota
    # ON organizations.id = ota.org_id

    # JOIN activities
    # ON ota.activity_type_id = activities.id
    # WHERE organizations.id =:org_id;"""

    stmt = select(Organization).where(
        Organization.id == org_id
    ).options(
        selectinload(Organization.activity_types),
        selectinload(Organization.phone_numbers),
        selectinload(Organization.building)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()



async def search_orgs_in_rectangle(
        lat_1: float,
        lon_1: float,
        lat_2: float,
        lon_2: float,
        db: AsyncSession
):
    lat_min, lat_max = sorted([lat_1, lat_2])
    lon_min, lon_max = sorted([lon_1, lon_2])

    stmt = select(Organization, Building).join(Building).filter(
        func.ST_Within(
            Building.location.cast(Geometry(geometry_type="POINT", srid=4326)),
            func.ST_MakeEnvelope(lon_min, lat_min, lon_max, lat_max, 4326)
        )
    )

    return (await db.execute(stmt)).all()


async def search_orgs_in_radius(
        lat: float,
        lon: float,
        radius_meters: int,
        db: AsyncSession
):
    stmt = select(Organization, Building).join(Building).filter(
        func.ST_DWithin(Building.location, func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), radius_meters)
    )

    return (await db.execute(stmt)).all()


async def list_orgs_children_to_activity(
        activity_id: int,
        db: AsyncSession
):
    activity_ids = await get_activity_and_children_ids(activity_id, db)
    if not activity_ids:
        return []

    stmt = select(Organization).join(Organization.activity_types).filter(Activity.id.in_(activity_ids)).distinct()
    return (await db.execute(stmt)).all()


async def search_orgs_by_name(
        search_string: str,
        db: AsyncSession
):
    stmt = select(Organization).where(Organization.title.ilike(f"%{search_string}%"))
    return (await db.execute(stmt)).all()
