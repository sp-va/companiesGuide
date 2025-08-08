import typing as t

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import db_session
from app.services.buildings import list_orgs_in_building
from app.schemas.organizations import OrganizationResponseModel

router = APIRouter(
    prefix="/buildings"
)


@router.get("/{building_id}/orgs")
async def list_building_orgs_endpoint(building_id: int, db: AsyncSession = Depends(db_session)) -> t.List[OrganizationResponseModel]:
    """Получение списка организаций, находящихся в конкретном здании

    Args:
        building_id (int): идентификатор здания

    Returns:
        t.List[OrganizationResponseModel]: Массив объектов с инентификаторами и названиями организаций
    """
    result = await list_orgs_in_building(building_id, db)

    return [OrganizationResponseModel(id=o.id, title=o.title) for o in result]