import typing as t

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import db_session
from app.services.organizations import get_org_full_info, list_orgs_of_exact_activity, search_orgs_by_name, search_orgs_in_radius, search_orgs_in_rectangle
from app.schemas.organizations import OrganizationResponseModel, OrganizationWithBuildingResponseModel, OrgsAndBuildingsResponseModel
from app.schemas.buildings import BuildingResponseModel


router = APIRouter(
    prefix="/orgs"
)


@router.get("/search")
async def search_org_by_name_endpoint(q: str, db: AsyncSession = Depends(db_session)) -> t.List[OrganizationResponseModel]:
    """Поиск организаций по названию

    Args:
        q (str): Строка, по которой выполняется поиск

    Returns:
        t.List[OrganizationResponseModel]: Массив объектов с инентификаторами и названиями организаций
    """
    result = await search_orgs_by_name(q, db)

    return [OrganizationResponseModel(id=o[0].id, title=o[0].title) for o in result]


@router.get("/location")
async def search_org_by_location_endpoint(
    lat_1: float,
    lon_1: float,
    radius_meters: t.Optional[int] = None,
    lat_2: t.Optional[float] = None,
    lon_2: t.Optional[float] = None,
    db: AsyncSession = Depends(db_session),
) -> OrgsAndBuildingsResponseModel:
    """Получение организаций и зданий в указанной прямоугольной (либо радиальной) области

    Args:
        lat_1 (float): Широта первой точки
        lon_1 (float): Долгота второй точки
        radius_meters (t.Optional[int], optional): Радиус окружности. Defaults to None.
        lat_2 (t.Optional[float], optional): Широта второй точки. Defaults to None.
        lon_2 (t.Optional[float], optional): Долгота второй точки. Defaults to None.

    Returns:
        OrgsAndBuildingsResponseModel: Объект с двумя массивами: строяния и организации
    """
    added_buildings = set()
    response = OrgsAndBuildingsResponseModel()
    result = []

    if lat_2 is not None and lon_2 is not None:
        result = await search_orgs_in_rectangle(lat_1, lon_1, lat_2, lon_2, db)

    elif radius_meters is not None:
        result = await search_orgs_in_radius(lat_1, lon_1, radius_meters, db)

    if len(result) != 0:
        for i in result:
            response.orgs.append(OrganizationWithBuildingResponseModel(
                id=i[0].id,
                title=i[0].title,
                building_id=i[0].building_id
            ))

            if i[1].id not in added_buildings:
                response.buildings.append(
                    BuildingResponseModel(
                        id=i[1].id,
                        address=i[1].address
                    )
                )
                added_buildings.add(i[1].id)
    return response

@router.get ("/{org_id}")
async def get_org_info_by_id_endpoint(org_id: int, db: AsyncSession = Depends(db_session)) -> t.Optional[t.Dict]:
    """Получение полной информации о конкретной организации

    Args:
        org_id (int): Идентификатор органзиации

    Returns:
        t.Optional[t.Dict]: Сведения об организации
    """
    org_info = await get_org_full_info(org_id, db)

    if org_info:
        result = {
            "id": org_info.id,
            "title": org_info.title,
            "address": org_info.building.address,
            "activities": [a.name for a in org_info.activity_types],
            "phone_numbers": [pn.number for pn in org_info.phone_numbers]
        }
    else:
        result = None

    return result
