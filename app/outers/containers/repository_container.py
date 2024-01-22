from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.datastore_container import DatastoreContainer
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
    datastores: DatastoreContainer = providers.DependenciesContainer()

    account: AccountRepository = providers.Singleton(
        AccountRepository,
        one_datastore=datastores.one_datastore
    )
    document_process: DocumentProcessRepository = providers.Singleton(
        DocumentProcessRepository,
        one_datastore=datastores.one_datastore
    )
    document: DocumentRepository = providers.Singleton(
        DocumentRepository,
        one_datastore=datastores.one_datastore
    )
    document_type: DocumentTypeRepository = providers.Singleton(
        DocumentTypeRepository,
        one_datastore=datastores.one_datastore
    )
    file_document: FileDocumentRepository = providers.Singleton(
        FileDocumentRepository,
        one_datastore=datastores.one_datastore
    )
    text_document: TextDocumentRepository = providers.Singleton(
        TextDocumentRepository,
        one_datastore=datastores.one_datastore
    )
    web_document: WebDocumentRepository = providers.Singleton(
        WebDocumentRepository,
        one_datastore=datastores.one_datastore
    )
