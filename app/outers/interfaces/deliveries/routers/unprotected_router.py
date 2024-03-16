from fastapi import APIRouter

from app.outers.interfaces.deliveries.controllers import authentication_controller

unprotected_router = APIRouter(
    prefix="",
    tags=["unprotected"]
)

unprotected_router.include_router(authentication_controller.router)
