import hashlib
import pathlib
import uuid
from typing import List

import tests
from apps.inners.models.daos.file_document import FileDocument
from tests.mocks.document_mock import DocumentMock


class FileDocumentMock:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock
        file_0_path = pathlib.Path(tests.__name__) / "mocks" / "files" / "file.pdf"
        file_0 = open(file_0_path, "rb")
        file_0_data = file_0.read()
        file_0.close()
        file_1_path = pathlib.Path(tests.__name__) / "mocks" / "files" / "file.txt"
        file_1 = open(file_1_path, "rb")
        file_1_data = file_1.read()
        file_1.close()
        self.file_data: List[bytes] = list(map(bytes, [file_0_data, file_1_data]))
        self._data: List[FileDocument] = [
            FileDocument(
                id=self.document_mock.data[0].id,
                file_name=f"{uuid.uuid4()}{file_0_path.suffix}",
                file_data_hash=hashlib.sha256(bytes(file_0_data)).hexdigest()
            ),
            FileDocument(
                id=self.document_mock.data[3].id,
                file_name=f"{uuid.uuid4()}{file_1_path.suffix}",
                file_data_hash=hashlib.sha256(bytes(file_1_data)).hexdigest()
            ),
        ]

    @property
    def data(self) -> List[FileDocument]:
        return [FileDocument(**file_document.dict()) for file_document in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for file_document in self._data:
            if file_document.id == id:
                is_found = True
                self._data.remove(file_document)

        if not is_found:
            raise ValueError(f"FileDocument with id {id} is not found.")