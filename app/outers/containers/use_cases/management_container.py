from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.managements.account_management import AccountManagement
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.session_management import SessionManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement


class ManagementContainer(DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    account = providers.Singleton(
        AccountManagement,
        account_repository=repositories.account,
    )
    session = providers.Singleton(
        SessionManagement,
        session_repository=repositories.session,
    )
    document = providers.Singleton(
        DocumentManagement,
        document_repository=repositories.document,
    )
    document_process = providers.Singleton(
        DocumentProcessManagement,
        document_process_repository=repositories.document_process,
    )
    document_type = providers.Singleton(
        DocumentTypeManagement,
        document_type_repository=repositories.document_type,
    )
    file_document = providers.Singleton(
        FileDocumentManagement,
        document_management=document,
        file_document_repository=repositories.file_document,
    )
    text_document = providers.Singleton(
        TextDocumentManagement,
        document_management=document,
        text_document_repository=repositories.text_document,
    )
    web_document = providers.Singleton(
        WebDocumentManagement,
        document_management=document,
        web_document_repository=repositories.web_document,
    )
