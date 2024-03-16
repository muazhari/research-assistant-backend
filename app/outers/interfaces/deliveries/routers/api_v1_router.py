from fastapi import APIRouter

from app.outers.interfaces.deliveries.routers.protected_router import protected_router
from app.outers.interfaces.deliveries.routers.unprotected_router import unprotected_router

api_v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

api_v1_router.include_router(protected_router)
api_v1_router.include_router(unprotected_router)
