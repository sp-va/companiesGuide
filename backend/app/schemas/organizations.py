import typing as t

from pydantic import BaseModel, Field

from app.schemas.buildings import BuildingResponseModel

class OrganizationResponseModel(BaseModel):
    id: int
    title: str


class OrganizationWithBuildingResponseModel(OrganizationResponseModel):
    building_id: int


class OrgsAndBuildingsResponseModel(BaseModel):
    orgs: t.Optional[t.List[OrganizationWithBuildingResponseModel]] = Field(default_factory=list)
    buildings: t.Optional[t.List[BuildingResponseModel]] = Field(default_factory=list)