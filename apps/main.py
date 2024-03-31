from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.container import application_container
from apps.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from apps.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware

app: FastAPI = FastAPI(
    title="research-assistant-backend",
    version="0.0.2"
)

app.container = application_container

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
    router=application_container.routers.api().router
)
