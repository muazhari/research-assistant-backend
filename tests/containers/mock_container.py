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
    account_mock = providers.Singleton(
        AccountMock
    )
    session_mock = providers.Singleton(
        SessionMock,
        account_mock=account_mock
    )
    document_type_mock = providers.Singleton(
        DocumentTypeMock
    )
    document_mock = providers.Singleton(
        DocumentMock,
        account_mock=account_mock,
        document_type_mock_data=document_type_mock
    )
    document_process_mock = providers.Singleton(
        DocumentProcessMock,
        document_mock=document_mock
    )
    text_document_mock = providers.Singleton(
        TextDocumentMock,
        document_mock=document_mock
    )
    file_document_mock = providers.Singleton(
        FileDocumentMock,
        document_mock=document_mock
    )
    web_document_mock = providers.Singleton(
        WebDocumentMock,
        document_mock=document_mock
    )
