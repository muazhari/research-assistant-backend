import hashlib
import uuid
from typing import List

from app.inners.models.daos.web_document import WebDocument
from test.mocks.document_mock import DocumentMock


class WebDocumentMock:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock
        web_url_0 = "https://www.google.com"
        web_url_1 = "https://www.bing.com"
        self._data: List[WebDocument] = [
            WebDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[0].id,
                web_url=web_url_0,
                web_url_hash=hashlib.sha256(web_url_0.encode()).digest()
            ),
            WebDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[3].id,
                web_url=web_url_1,
                web_url_hash=hashlib.sha256(web_url_1.encode()).digest()
            ),
        ]

    @property
    def data(self) -> List[WebDocument]:
        return [WebDocument(**web_document.dict()) for web_document in self._data]
