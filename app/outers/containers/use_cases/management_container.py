from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.managements.account_management import AccountManagement
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.outers.containers.repository_container import RepositoryContainer
from app.outers.containers.setting_container import SettingContainer
from app.outers.containers.use_cases.utility_container import UtilityContainer


class ManagementContainer(DeclarativeContainer):
    settings: SettingContainer = providers.DependenciesContainer()
    repositories: RepositoryContainer = providers.DependenciesContainer()
    utilities: UtilityContainer = providers.DependenciesContainer()

    account: AccountManagement = providers.Singleton(
        AccountManagement,
        account_repository=repositories.account,
        management_utility=utilities.management
    )
    document: DocumentManagement = providers.Singleton(
        DocumentManagement,
        document_repository=repositories.document,
        management_utility=utilities.management
    )
    document_process: DocumentProcessManagement = providers.Singleton(
        DocumentProcessManagement,
        document_process_repository=repositories.document_process,
        management_utility=utilities.management
    )
    document_type: DocumentTypeManagement = providers.Singleton(
        DocumentTypeManagement,
        document_type_repository=repositories.document_type,
        management_utility=utilities.management
    )
    file_document: FileDocumentManagement = providers.Singleton(
        FileDocumentManagement,
        document_repository=repositories.document,
        file_document_repository=repositories.file_document,
        management_utility=utilities.management,
        document_conversion_utility=utilities.document_conversion,
        temp_persistence_setting=settings.temp_persistence
    )
    text_document: TextDocumentManagement = providers.Singleton(
        TextDocumentManagement,
        document_repository=repositories.document,
        text_document_repository=repositories.text_document,
        management_utility=utilities.management,
    )
    web_document: WebDocumentManagement = providers.Singleton(
        WebDocumentManagement,
        document_repository=repositories.document,
        web_document_repository=repositories.web_document,
        management_utility=utilities.management,
    )
