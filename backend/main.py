import asyncio
from fastapi import FastAPI

from app.services.add_init_data import add_init_data
from app.routes.buildings import router as buildings_router
from app.routes.orgs import router as orgs_router
from app.routes.activities import router as activities_router


async def startup_event():
    await add_init_data()

app = FastAPI(
    root_path="/api/v1",
    on_startup=[startup_event,]
)


app.include_router(buildings_router)
app.include_router(orgs_router)
app.include_router(activities_router)
