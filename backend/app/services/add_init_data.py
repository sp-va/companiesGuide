import json
from geoalchemy2 import WKTElement
from sqlalchemy.exc import IntegrityError

from app.db.connect import session_maker
from app.models.activity_type import Activity
from app.models.building import Building
from app.models.organization import Organization, PhoneNumber


async def add_init_data():
    session = session_maker.db_session()

    async with session:
        try:
            with open("./app/init_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

                for b in data.get("buildings", []):
                    building = Building(
                        id=b["id"],
                        address=b["address"],
                        location=WKTElement(f'POINT({b["location"][1]} {b["location"][0]})', srid=4326)
                    )
                    session.add(building)
                await session.flush()

                activity_map = {}
                for a in data.get("activities", []):
                    activity = Activity(
                        id=a["id"],
                        name=a["name"],
                        parent_id=a["parent_id"]
                    )
                    session.add(activity)
                    activity_map[a["id"]] = activity
                await session.flush()

                for o in data.get("organizations", []):
                    linked_activities = [activity_map[aid] for aid in o.get("activity_ids", [])]

                    org = Organization(
                        title=o["title"],
                        building_id=o.get("building_id"),
                        activity_types=linked_activities
                    )
                    session.add(org)
                    await session.flush()

                    for num in o.get("phone_numbers", []):
                        phone = PhoneNumber(
                            number=num,
                            related_org=org.id
                        )
                        session.add(phone)

                await session.commit()

        except IntegrityError as e:
            await session.rollback()