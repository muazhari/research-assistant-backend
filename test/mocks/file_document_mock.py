import hashlib
import pathlib
import uuid
from typing import List

from app.inners.models.daos.file_document import FileDocument
from test.mocks.document_mock import DocumentMock


class FileDocumentMock:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock
        file_0_path = pathlib.Path("test/mocks") / "files" / "file.txt"
        file_0 = open(file_0_path, "rb")
        file_0_data = file_0.read()
        file_0_data_hash: bytes = hashlib.sha256(file_0_data).digest()
        file_0.close()
        file_1_path = pathlib.Path("test/mocks") / "files" / "file.pdf"
        file_1 = open(file_1_path, "rb")
        file_1_data = file_1.read()
        file_1_data_hash: bytes = hashlib.sha256(file_1_data).digest()
        file_1.close()
        self._data: List[FileDocument] = [
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[0].id,
                file_name=file_0.name,
                file_extension=file_0_path.suffix,
                file_data=file_0_data.hex(),
                file_data_hash=file_0_data_hash
            ),
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[3].id,
                file_name=file_0.name,
                file_extension=file_0_path.suffix,
                file_data=file_0_data.hex(),
                file_data_hash=file_0_data_hash
            ),
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[1].id,
                file_name=file_1.name,
                file_extension=file_1_path.suffix,
                file_data=file_1_data.hex(),
                file_data_hash=file_1_data_hash
            ),
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock.data[4].id,
                file_name=file_1.name,
                file_extension=file_1_path.suffix,
                file_data=file_1_data.hex(),
                file_data_hash=file_1_data_hash
            ),
        ]

    @property
    def data(self) -> List[FileDocument]:
        return [FileDocument(**file_document.dict()) for file_document in self._data]
