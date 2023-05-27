from fastapi import APIRouter

from app.outers.interfaces.deliveries.controllers import account_controller, \
    document_type_controller, document_controller, document_process_controller, file_document_controller, \
    text_document_controller, web_document_controller, passage_search_controller

api_v1_router = APIRouter(prefix="/v1", tags=["v1"])

api_v1_router.include_router(account_controller.router)
api_v1_router.include_router(document_process_controller.router)
api_v1_router.include_router(document_type_controller.router)
api_v1_router.include_router(file_document_controller.router)
api_v1_router.include_router(text_document_controller.router)
api_v1_router.include_router(web_document_controller.router)
api_v1_router.include_router(document_controller.router)

api_v1_router.include_router(passage_search_controller.router)
