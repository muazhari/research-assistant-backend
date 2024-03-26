from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.repositories.account_repository import AccountRepository
from apps.outers.repositories.document_process_repository import DocumentProcessRepository
from apps.outers.repositories.document_repository import DocumentRepository
from apps.outers.repositories.document_type_repository import DocumentTypeRepository
from apps.outers.repositories.file_document_repository import FileDocumentRepository
from apps.outers.repositories.session_repository import SessionRepository
from apps.outers.repositories.text_document_repository import TextDocumentRepository
from apps.outers.repositories.web_document_repository import WebDocumentRepository


class RepositoryContainer(DeclarativeContainer):
    datastores = providers.DependenciesContainer()

    account = providers.Singleton(
        AccountRepository
    )
    session = providers.Singleton(
        SessionRepository
    )
    document_process = providers.Singleton(
        DocumentProcessRepository
    )
    document = providers.Singleton(
        DocumentRepository
    )
    document_type = providers.Singleton(
        DocumentTypeRepository
    )
    file_document = providers.Singleton(
        FileDocumentRepository,
        three_datastore=datastores.three_datastore
    )
    text_document = providers.Singleton(
        TextDocumentRepository
    )
    web_document = providers.Singleton(
        WebDocumentRepository
    )
