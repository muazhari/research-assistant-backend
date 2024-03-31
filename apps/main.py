from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps import inners, outers
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from apps.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from apps.outers.interfaces.deliveries.routers.api_router import api_router

app: FastAPI = FastAPI(
    title="research-assistant-backend",
    version="0.0.2"
)

application_container: ApplicationContainer = ApplicationContainer()
app.container = application_container
app.container.wire(packages=[inners, outers])

app.add_middleware(
    middleware_class=AuthorizationMiddleware,
    session_management=app.container.use_cases.managements.session()
)

app.add_middleware(
    middleware_class=SessionMiddleware,
    one_datastore=app.container.datastores.one()
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    router=api_router
)
