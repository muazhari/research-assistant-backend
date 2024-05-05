from typing import List

from apps.inners.models.daos.document_type import DocumentType


class DocumentTypeFake:

    def __init__(self):
        self._data: List[DocumentType] = [
            DocumentType(
                id="file",
                description="description1",
            ),
            DocumentType(
                id="text",
                description="description0",
            ),
            DocumentType(
                id="web",
                description="description2",
            )
        ]

    @property
    def data(self) -> List[DocumentType]:
        return [DocumentType(**document_type.model_dump()) for document_type in self._data]
