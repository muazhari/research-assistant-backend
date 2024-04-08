import hashlib
import uuid
from typing import List

from apps.inners.models.daos.web_document import WebDocument
from tests.fakes.document_fake import DocumentFake


class WebDocumentFake:

    def __init__(
            self,
            document_fake: DocumentFake
    ):
        self.document_fake: DocumentFake = document_fake
        web_url_0 = "https://www.google.com"
        web_url_1 = "https://www.bing.com"
        self._data: List[WebDocument] = [
            WebDocument(
                id=self.document_fake.data[2].id,
                web_url=web_url_0,
                web_url_hash=hashlib.sha256(web_url_0.encode()).hexdigest()
            ),
            WebDocument(
                id=self.document_fake.data[5].id,
                web_url=web_url_1,
                web_url_hash=hashlib.sha256(web_url_1.encode()).hexdigest()
            ),
        ]

    @property
    def data(self) -> List[WebDocument]:
        return [WebDocument(**web_document.dict()) for web_document in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for web_document in self._data:
            if web_document.id == id:
                is_found = True
                self._data.remove(web_document)

        if not is_found:
            raise ValueError(f"WebDocument with id {id} is not found.")
