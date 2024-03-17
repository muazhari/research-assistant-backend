from uuid import UUID

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig
from starlette.middleware.cors import CORSMiddleware

from app import inners, outers
from app.outers.containers.application_container import ApplicationContainer
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
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

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    middleware_class=SessionMiddleware,
    one_datastore=app.container.datastores.one_datastore()

)

# app.add_middleware(
#     middleware_class=AuthorizationMiddleware,
# )

app.include_router(
    router=api_router
)
