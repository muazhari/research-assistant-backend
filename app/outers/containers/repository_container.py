from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.repositories.account_repository import AccountRepository
from app.outers.repositories.document_process_repository import DocumentProcessRepository
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.repositories.document_type_repository import DocumentTypeRepository
from app.outers.repositories.file_document_repository import FileDocumentRepository
from app.outers.repositories.text_document_repository import TextDocumentRepository
from app.outers.repositories.web_document_repository import WebDocumentRepository


class RepositoryContainer(DeclarativeContainer):
    account = providers.Singleton(
        AccountRepository
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
        FileDocumentRepository
    )
    text_document = providers.Singleton(
        TextDocumentRepository
    )
    web_document = providers.Singleton(
        WebDocumentRepository
    )
