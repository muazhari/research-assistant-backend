from fastapi import APIRouter

from app.infrastucture.delivery.controller import passage_search_controller

api_router = APIRouter(prefix="/api/v1")

search_api_router = APIRouter(prefix="/search")
search_api_router.include_router(passage_search_controller.router, prefix="/passage")

document_transfer_api_router = APIRouter(prefix="/document-transfer")

api_router.include_router(search_api_router)
api_router.include_router(document_transfer_api_router)
