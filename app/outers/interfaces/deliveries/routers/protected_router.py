from fastapi import APIRouter
from starlette.middleware import Middleware

from app.outers.interfaces.deliveries.controllers import account_controller, document_process_controller, \
    document_type_controller, file_document_controller, text_document_controller, web_document_controller, \
    document_controller, passage_search_controller, long_form_qa_controller
from app.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from app.outers.interfaces.deliveries.middlewares.wrapper_middleware import MiddlewareWrapper

protected_router = APIRouter(
    prefix="",
    tags=["protected"],
    route_class=MiddlewareWrapper(
        middleware=[
            Middleware(
                cls=AuthorizationMiddleware
            )
        ]
    )
)

protected_router.include_router(account_controller.router)
protected_router.include_router(document_process_controller.router)
protected_router.include_router(document_type_controller.router)
protected_router.include_router(file_document_controller.router)
protected_router.include_router(text_document_controller.router)
protected_router.include_router(web_document_controller.router)
protected_router.include_router(document_controller.router)
protected_router.include_router(passage_search_controller.router)
protected_router.include_router(long_form_qa_controller.router)
