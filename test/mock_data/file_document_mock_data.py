import uuid

from app.inners.models.entities.file_document import FileDocument
from test.mock_data.document_mock_data import DocumentMockData


class FileDocumentMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.document_data = self.document_mock_data.get_data()

    def get_data(self) -> dict:
        return {
            "account": self.document_data["account"],
            "document_type": self.document_data["document_type"],
            "document": self.document_data["document"],
            "file_document": [
                FileDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][0].id,
                    file_name="file_name_1",
                    file_extension="file_extension_1",
                    file_bytes=b"file_bytes_1",
                ),
                FileDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][1].id,
                    file_name="file_name_2",
                    file_extension="file_extension_2",
                    file_bytes=b"file_bytes_2",
                )
            ]
        }
