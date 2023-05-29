import uuid
from typing import List

from app.inners.models.entities.file_document import FileDocument
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from test.mock_data.document_mock_data import DocumentMockData


class FileDocumentMockData:

    def __init__(self):
        self.document_mock_data: DocumentMockData = DocumentMockData()
        self.data: List[FileDocument] = [
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[0].id,
                file_name="file_name_0",
                file_extension="file_extension_0",
                file_bytes=b"file_bytes_0",
            ),
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[1].id,
                file_name="file_name_1",
                file_extension="file_extension_1",
                file_bytes=b"file_bytes_1",
            )
        ]
        self.response_data: List[FileDocumentResponse] = [
            FileDocumentResponse(
                id=self.document_mock_data.data[0].id,
                name=self.document_mock_data.data[0].name,
                description=self.document_mock_data.data[0].description,
                document_type_id=self.document_mock_data.data[0].document_type_id,
                account_id=self.document_mock_data.data[0].account_id,
                file_name=self.data[0].file_name,
                file_extension=self.data[0].file_extension,
                file_bytes=self.data[0].file_bytes,
            ),
            FileDocumentResponse(
                id=self.document_mock_data.data[1].id,
                name=self.document_mock_data.data[1].name,
                description=self.document_mock_data.data[1].description,
                document_type_id=self.document_mock_data.data[1].document_type_id,
                account_id=self.document_mock_data.data[1].account_id,
                file_name=self.data[1].file_name,
                file_extension=self.data[1].file_extension,
                file_bytes=self.data[1].file_bytes,
            )
        ]
