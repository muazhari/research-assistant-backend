from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from test.seeders.account_seeder import AccountSeeder
from test.seeders.all_seeder import AllSeeder
from test.seeders.document_process_seeder import DocumentProcessSeeder
from test.seeders.document_seeder import DocumentSeeder
from test.seeders.document_type_seeder import DocumentTypeSeeder
from test.seeders.file_document_seeder import FileDocumentSeeder
from test.seeders.session_seeder import SessionSeeder
from test.seeders.text_document_seeder import TextDocumentSeeder
from test.seeders.web_document_seeder import WebDocumentSeeder


class SeederContainer(DeclarativeContainer):
    datastores = providers.DependenciesContainer()
    mocks = providers.DependenciesContainer()

    account_seeder = providers.Singleton(
        AccountSeeder,
        account_mock=mocks.account_mock
    )

    session_seeder = providers.Singleton(
        SessionSeeder,
        session_mock=mocks.session_mock
    )

    document_type_seeder = providers.Singleton(
        DocumentTypeSeeder,
        document_type_mock=mocks.document_type_mock
    )

    document_seeder = providers.Singleton(
        DocumentSeeder,
        document_mock=mocks.document_mock
    )

    document_process_seeder = providers.Singleton(
        DocumentProcessSeeder,
        document_process_mock=mocks.document_process_mock
    )

    text_document_seeder = providers.Singleton(
        TextDocumentSeeder,
        text_document_mock=mocks.text_document_mock
    )

    file_document_seeder = providers.Singleton(
        FileDocumentSeeder,
        file_document_mock=mocks.file_document_mock
    )

    web_document_seeder = providers.Singleton(
        WebDocumentSeeder,
        web_document_mock=mocks.web_document_mock
    )

    all_seeder = providers.Singleton(
        AllSeeder,
        one_datastore=datastores.one_datastore,
        account_seeder=account_seeder,
        document_type_seeder=document_type_seeder,
        document_seeder=document_seeder,
        document_process_seeder=document_process_seeder,
        text_document_seeder=text_document_seeder,
        file_document_seeder=file_document_seeder,
        web_document_seeder=web_document_seeder
    )
