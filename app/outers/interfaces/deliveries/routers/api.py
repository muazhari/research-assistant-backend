from fastapi import APIRouter

from app.outers.interfaces.deliveries.routers.api_v1 import api_v1_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(api_v1_router)
