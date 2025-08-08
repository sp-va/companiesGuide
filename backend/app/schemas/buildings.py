from pydantic import BaseModel

class BuildingResponseModel(BaseModel):
    id: int
    address: str