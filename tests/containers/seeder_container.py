from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from tests.seeders.account_seeder import AccountSeeder
from tests.seeders.all_seeder import AllSeeder
from tests.seeders.document_process_seeder import DocumentProcessSeeder
from tests.seeders.document_seeder import DocumentSeeder
from tests.seeders.document_type_seeder import DocumentTypeSeeder
from tests.seeders.file_document_seeder import FileDocumentSeeder
from tests.seeders.session_seeder import SessionSeeder
from tests.seeders.text_document_seeder import TextDocumentSeeder
from tests.seeders.web_document_seeder import WebDocumentSeeder


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
        file_document_mock=mocks.file_document_mock,
        three_datastore=datastores.three_datastore
    )

    web_document_seeder = providers.Singleton(
        WebDocumentSeeder,
        web_document_mock=mocks.web_document_mock
    )

    all_seeder = providers.Singleton(
        AllSeeder,
        one_datastore=datastores.one_datastore,
        account_seeder=account_seeder,
        session_seeder=session_seeder,
        document_type_seeder=document_type_seeder,
        document_seeder=document_seeder,
        document_process_seeder=document_process_seeder,
        text_document_seeder=text_document_seeder,
        file_document_seeder=file_document_seeder,
        web_document_seeder=web_document_seeder
    )
