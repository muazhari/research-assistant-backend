from fastapi import APIRouter

from apps.outers.interfaces.deliveries.routers.protected_router import protected_router
from apps.outers.interfaces.deliveries.routers.unprotected_router import unprotected_router

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

api_router.include_router(protected_router)
api_router.include_router(unprotected_router)
