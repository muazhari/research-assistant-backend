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

    account = providers.Singleton(
        AccountSeeder,
        account_mock=mocks.account
    )

    session = providers.Singleton(
        SessionSeeder,
        session_mock=mocks.session
    )

    document_type = providers.Singleton(
        DocumentTypeSeeder,
        document_type_mock=mocks.document_type
    )

    document = providers.Singleton(
        DocumentSeeder,
        document_mock=mocks.document
    )

    document_process = providers.Singleton(
        DocumentProcessSeeder,
        document_process_mock=mocks.document_process
    )

    text_document = providers.Singleton(
        TextDocumentSeeder,
        text_document_mock=mocks.text_document
    )

    file_document = providers.Singleton(
        FileDocumentSeeder,
        file_document_mock=mocks.file_document,
        three_datastore=datastores.three
    )

    web_document = providers.Singleton(
        WebDocumentSeeder,
        web_document_mock=mocks.web_document
    )

    all = providers.Singleton(
        AllSeeder,
        one_datastore=datastores.one,
        account_seeder=account,
        session_seeder=session,
        document_type_seeder=document_type,
        document_seeder=document,
        document_process_seeder=document_process,
        text_document_seeder=text_document,
        file_document_seeder=file_document,
        web_document_seeder=web_document
    )
