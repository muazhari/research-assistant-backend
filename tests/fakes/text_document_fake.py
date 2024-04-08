import hashlib
import uuid
from typing import List

from apps.inners.models.daos.text_document import TextDocument
from tests.fakes.document_fake import DocumentFake


class TextDocumentFake:

    def __init__(
            self,
            document_fake: DocumentFake
    ):
        self.document_fake: DocumentFake = document_fake
        text_content_0 = "Nervous system is a part of an animal's body that coordinates its actions and sensory information by transmitting signals to and from different parts of its body."
        text_content_1 = "Political science is the scientific study of politics. It is a social science dealing with systems of governance and power, and the analysis of political activities, political thoughts, political behavior, and political structures."
        self._data: List[TextDocument] = [
            TextDocument(
                id=self.document_fake.data[1].id,
                text_content=text_content_0,
                text_content_hash=hashlib.sha256(text_content_0.encode()).hexdigest()
            ),
            TextDocument(
                id=self.document_fake.data[4].id,
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
