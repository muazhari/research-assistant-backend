from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from tests.fakes.account_fake import AccountFake
from tests.fakes.document_fake import DocumentFake
from tests.fakes.document_process_fake import DocumentProcessFake
from tests.fakes.document_type_fake import DocumentTypeFake
from tests.fakes.file_document_fake import FileDocumentFake
from tests.fakes.session_fake import SessionFake
from tests.fakes.text_document_fake import TextDocumentFake
from tests.fakes.web_document_fake import WebDocumentFake


class FakeContainer(DeclarativeContainer):
    account = providers.Singleton(
        AccountFake
    )
    session = providers.Singleton(
        SessionFake,
        account_fake=account
    )
    document_type = providers.Singleton(
        DocumentTypeFake
    )
    document = providers.Singleton(
        DocumentFake,
        account_fake=account,
        document_type_fake_data=document_type
    )
    document_process = providers.Singleton(
        DocumentProcessFake,
        document_fake=document
    )
    text_document = providers.Singleton(
        TextDocumentFake,
        document_fake=document
    )
    file_document = providers.Singleton(
        FileDocumentFake,
        document_fake=document
    )
    web_document = providers.Singleton(
        WebDocumentFake,
        document_fake=document
    )
