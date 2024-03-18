import hashlib
import uuid
from typing import List

from app.inners.models.daos.text_document import TextDocument
from test.mocks.document_mock import DocumentMock


class TextDocumentMock:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock
        text_content_0 = "text0"
        text_content_1 = "text1"
        self._data: List[TextDocument] = [
            TextDocument(
                id=self.document_mock.data[1].id,
                text_content=text_content_0,
                text_content_hash=hashlib.sha256(text_content_0.encode()).hexdigest()
            ),
            TextDocument(
                id=self.document_mock.data[4].id,
                text_content=text_content_1,
                text_content_hash=hashlib.sha256(text_content_1.encode()).hexdigest()
            ),
        ]

    @property
    def data(self) -> List[TextDocument]:
        return [TextDocument(**text_document.dict()) for text_document in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for text_document in self._data:
            if text_document.id == id:
                is_found = True
                self._data.remove(text_document)

        if not is_found:
            raise ValueError(f"TextDocument with id {id} is not found.")
