from fastapi import APIRouter

from apps.outers.interfaces.deliveries.controllers.account_controller import AccountController
from apps.outers.interfaces.deliveries.controllers.authentication_controller import AuthenticationController
from apps.outers.interfaces.deliveries.controllers.authorization_controller import AuthorizationController
from apps.outers.interfaces.deliveries.controllers.document_controller import DocumentController
from apps.outers.interfaces.deliveries.controllers.document_process_controller import DocumentProcessController
from apps.outers.interfaces.deliveries.controllers.document_type_controller import DocumentTypeController
from apps.outers.interfaces.deliveries.controllers.file_document_controller import FileDocumentController
from apps.outers.interfaces.deliveries.controllers.long_form_qa_controller import LongFormQaController
from apps.outers.interfaces.deliveries.controllers.passage_search_controller import PassageSearchController
from apps.outers.interfaces.deliveries.controllers.text_document_controller import TextDocumentController
from apps.outers.interfaces.deliveries.controllers.web_document_controller import WebDocumentController


class ApiRouter:
    def __init__(
            self,
            authentication_controller: AuthenticationController,
            authorization_controller: AuthorizationController,
            account_controller: AccountController,
            document_controller: DocumentController,
            document_type_controller: DocumentTypeController,
            document_process_controller: DocumentProcessController,
            file_document_controller: FileDocumentController,
            text_document_controller: TextDocumentController,
            web_document_controller: WebDocumentController,
            passage_search_controller: PassageSearchController,
            long_form_qa_controller: LongFormQaController
    ):
        self.router = APIRouter(
            prefix="/api",
            tags=["api"]
        )
        self.router.include_router(authentication_controller.router)
        self.router.include_router(authorization_controller.router)
        self.router.include_router(account_controller.router)
        self.router.include_router(document_controller.router)
        self.router.include_router(document_type_controller.router)
        self.router.include_router(document_process_controller.router)
        self.router.include_router(file_document_controller.router)
        self.router.include_router(text_document_controller.router)
        self.router.include_router(web_document_controller.router)
        self.router.include_router(passage_search_controller.router)
        self.router.include_router(long_form_qa_controller.router)
