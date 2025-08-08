from sqlalchemy import select, union_all
from sqlalchemy.orm import aliased
from sqlalchemy.sql import column
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_type import Activity

async def get_activity_and_children_ids(activity_id: int, db: AsyncSession) -> list[int]:
    activity_alias = aliased(Activity)
    cte = select(Activity.id, Activity.parent_id).where(Activity.id == activity_id).cte(name="activity_tree", recursive=True)
    cte_alias = aliased(cte)
    children = select(activity_alias.id, activity_alias.parent_id).where(activity_alias.parent_id == cte_alias.c.id)
    cte = cte.union_all(children)

    result = await db.execute(select(cte.c.id))

    return result.scalars().all()
