from uuid import UUID

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig

from app import outers, inners
from app.outers.containers.application_container import ApplicationContainer
from app.outers.interfaces.deliveries.routers.api_router import api_router

BaseConfig.json_encoders = {
    UUID: jsonable_encoder,
}

app: FastAPI = FastAPI(
    title="research-assistant-backend",
    version="0.0.2"
)

app.container = ApplicationContainer()
app.container.wire(packages=[inners, outers])

app.include_router(
    router=api_router
)
