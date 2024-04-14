from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

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


class ControllerContainer(DeclarativeContainer):
    managements = providers.DependenciesContainer()
    authentications = providers.DependenciesContainer()
    authorizations = providers.DependenciesContainer()
    passage_searches = providers.DependenciesContainer()
    long_form_qas = providers.DependenciesContainer()

    account = providers.Singleton(
        AccountController,
        account_management=managements.account
    )
    authentication = providers.Singleton(
        AuthenticationController,
        login_authentication=authentications.login,
        register_authentication=authentications.register,
        logout_authentication=authentications.logout
    )
    authorization = providers.Singleton(
        AuthorizationController,
        session_authorization=authorizations.session,
    )
    document = providers.Singleton(
        DocumentController,
        document_management=managements.document
    )
    document_type = providers.Singleton(
        DocumentTypeController,
        document_type_management=managements.document_type
    )
    document_process = providers.Singleton(
        DocumentProcessController,
        document_process_management=managements.document_process
    )
    file_document = providers.Singleton(
        FileDocumentController,
        file_document_management=managements.file_document
    )
    text_document = providers.Singleton(
        TextDocumentController,
        text_document_management=managements.text_document
    )
    web_document = providers.Singleton(
        WebDocumentController,
        web_document_management=managements.web_document
    )
    passage_search = providers.Singleton(
        PassageSearchController,
        process_passage_search=passage_searches.process
    )
    long_form_qa = providers.Singleton(
        LongFormQaController,
        process_long_form_qa=long_form_qas.process
    )
