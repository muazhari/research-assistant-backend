from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from fastapi.security import HTTPBearer

from apps.outers.interfaces.deliveries.routers.api_router import ApiRouter


class RouterContainer(DeclarativeContainer):
    controllers = providers.DependenciesContainer()

    security = providers.Singleton(
        HTTPBearer,
        auto_error=False
    )
    api = providers.Singleton(
        ApiRouter,
        authentication_controller=controllers.authentication,
        authorization_controller=controllers.authorization,
        account_controller=controllers.account,
        document_controller=controllers.document,
        document_type_controller=controllers.document_type,
        document_process_controller=controllers.document_process,
        file_document_controller=controllers.file_document,
        text_document_controller=controllers.text_document,
        web_document_controller=controllers.web_document,
        passage_search_controller=controllers.passage_search,
        long_form_qa_controller=controllers.long_form_qa
    )
