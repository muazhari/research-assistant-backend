from typing import List

from app.inners.models.daos.document_type import DocumentType


class DocumentTypeMock:

    def __init__(self):
        self._data: List[DocumentType] = [
            DocumentType(
                id="text",
                description="description0",
            ),
            DocumentType(
                id="file",
                description="description1",
            ),
            DocumentType(
                id="web",
                description="description2",
            )
        ]

    @property
    def data(self) -> List[DocumentType]:
        return [DocumentType(**document_type.dict()) for document_type in self._data]

    def delete_many_by_id(self, id: str):
        is_found: bool = False
        for document_type in self._data:
            if document_type.id == id:
                is_found = True
                self._data.remove(document_type)

        if not is_found:
            raise ValueError(f"DocumentType with id {id} is not found.")
