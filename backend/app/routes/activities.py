import typing as t

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import db_session
from app.services.organizations import list_orgs_children_to_activity, list_orgs_of_exact_activity
from app.schemas.organizations import OrganizationResponseModel


router = APIRouter(
    prefix="/activities"
)


@router.get ("/{}")


@router.get("/{activity_id}/orgs")
async def list_exact_activity_orgs_endpoint(activity_id: int, db: AsyncSession = Depends(db_session)) -> t.List[OrganizationResponseModel]:
    """Получение списка организаций для конкретного вида деятельности

    Args:
        activity_id (int): идентификатор вида деятельности

    Returns:
        t.List[OrganizationResponseModel]: Массив объектов с инентификаторами и названиями организаций
    """
    result = await list_orgs_of_exact_activity(activity_id, db)
    return [OrganizationResponseModel(id=o.id, title=o.title) for o in result]


@router.get("")
async def get_all_children_endpoint(activity_id: int, db: AsyncSession = Depends(db_session)) -> t.List[OrganizationResponseModel]:
    result = await list_orgs_children_to_activity(activity_id, db)

    return [OrganizationResponseModel(id=o[0].id, title=o[0].title) for o in result]