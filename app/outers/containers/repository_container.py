from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.persistence_container import PersistenceContainer
from app.outers.containers.setting_container import SettingContainer
from app.outers.repositories.account_repository import AccountRepository
from app.outers.repositories.document_process_repository import DocumentProcessRepository
from app.outers.repositories.document_repository import DocumentRepository
from app.outers.repositories.document_type_repository import DocumentTypeRepository
from app.outers.repositories.file_document_repository import FileDocumentRepository
from app.outers.repositories.text_document_repository import TextDocumentRepository
from app.outers.repositories.web_document_repository import WebDocumentRepository


class RepositoryContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    persistences: PersistenceContainer = providers.DependenciesContainer()

    account: AccountRepository = providers.Singleton(
        AccountRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    document_process: DocumentProcessRepository = providers.Singleton(
        DocumentProcessRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    document: DocumentRepository = providers.Singleton(
        DocumentRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    document_type: DocumentTypeRepository = providers.Singleton(
        DocumentTypeRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    file_document: FileDocumentRepository = providers.Singleton(
        FileDocumentRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    text_document: TextDocumentRepository = providers.Singleton(
        TextDocumentRepository,
        datastore_one_persistence=persistences.datastore_one
    )
    web_document: WebDocumentRepository = providers.Singleton(
        WebDocumentRepository,
        datastore_one_persistence=persistences.datastore_one
    )
