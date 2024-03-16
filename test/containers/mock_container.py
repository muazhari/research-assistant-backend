from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from test.mocks.account_mock import AccountMock
from test.mocks.document_mock import DocumentMock
from test.mocks.document_process_mock import DocumentProcessMock
from test.mocks.document_type_mock import DocumentTypeMock
from test.mocks.file_document_mock import FileDocumentMock
from test.mocks.session_mock import SessionMock
from test.mocks.text_document_mock import TextDocumentMock
from test.mocks.web_document_mock import WebDocumentMock


class MockContainer(DeclarativeContainer):
    account_mock = providers.Singleton(
        AccountMock
    )
    session_mock = providers.Singleton(
        SessionMock
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
