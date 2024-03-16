from fastapi import APIRouter
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware
from app.outers.interfaces.deliveries.middlewares.wrapper_middleware import MiddlewareWrapper
from app.outers.interfaces.deliveries.routers.api_v1_router import api_v1_router

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
    route_class=MiddlewareWrapper(
        middleware=[
            Middleware(
                cls=CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            ),
            Middleware(
                cls=SessionMiddleware
            )
        ]
    )
)

api_router.include_router(api_v1_router)
