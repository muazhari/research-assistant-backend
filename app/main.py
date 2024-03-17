from uuid import UUID

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig
from starlette.middleware.cors import CORSMiddleware

from app import inners, outers
from app.outers.containers.application_container import ApplicationContainer
from app.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware

BaseConfig.json_encoders = {
    UUID: jsonable_encoder,
}

app: FastAPI = FastAPI(
    title="research-assistant-backend",
    version="0.0.2"
)

app_protected = FastAPI(
    title="research-assistant-backend-protected",
    version="0.0.2"
)

app_unprotected = FastAPI(
    title="research-assistant-backend-unprotected",
    version="0.0.2"
)

path: str = "/api/v1"

app.mount(
    path=path,
    app=app_protected
)

app.mount(
    path=path,
    app=app_unprotected
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

app_protected.add_middleware(
    middleware_class=AuthorizationMiddleware,
)
