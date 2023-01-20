from fastapi import APIRouter

from app.outer.interfaces.deliveries.controllers import passage_search_controller, account_controller, \
    document_type_controller, document_controller, document_process_controller, file_document_controller, \
    text_document_controller, web_document_controller
from app.outer.interfaces.deliveries.routers.api_v1 import api_v1_router

api_router = APIRouter(prefix="/api")

api_router.include_router(api_v1_router)
