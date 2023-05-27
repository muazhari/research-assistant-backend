import uuid

from app.inners.models.entities.document_process import DocumentProcess
from test.mock_data.document_mock_data import DocumentMockData


class DocumentProcessMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.document_data = self.document_mock_data.get_data()

    def get_data(self) -> dict:
        return {
            "account": self.document_data["account"],
            "document_type": self.document_data["document_type"],
            "document": self.document_data["document"],
            "document_process": [
                DocumentProcess(
                    id=uuid.uuid4(),
                    initial_document_id=self.document_data["document"][0].id,
                    final_document_id=self.document_data["document"][1].id,
                    process_duration=0.0,
                ),
                DocumentProcess(
                    id=uuid.uuid4(),
                    initial_document_id=self.document_data["document"][1].id,
                    final_document_id=self.document_data["document"][0].id,
                    process_duration=1.0,
                )
            ]

        }
