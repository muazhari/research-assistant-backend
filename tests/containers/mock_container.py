from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from tests.mocks.account_mock import AccountMock
from tests.mocks.document_mock import DocumentMock
from tests.mocks.document_process_mock import DocumentProcessMock
from tests.mocks.document_type_mock import DocumentTypeMock
from tests.mocks.file_document_mock import FileDocumentMock
from tests.mocks.session_mock import SessionMock
from tests.mocks.text_document_mock import TextDocumentMock
from tests.mocks.web_document_mock import WebDocumentMock


class MockContainer(DeclarativeContainer):
    account = providers.Singleton(
        AccountMock
    )
    session = providers.Singleton(
        SessionMock,
        account_mock=account
    )
    document_type = providers.Singleton(
        DocumentTypeMock
    )
    document = providers.Singleton(
        DocumentMock,
        account_mock=account,
        document_type_mock_data=document_type
    )
    document_process = providers.Singleton(
        DocumentProcessMock,
        document_mock=document
    )
    text_document = providers.Singleton(
        TextDocumentMock,
        document_mock=document
    )
    file_document = providers.Singleton(
        FileDocumentMock,
        document_mock=document
    )
    web_document = providers.Singleton(
        WebDocumentMock,
        document_mock=document
    )
