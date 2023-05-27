import uuid

from app.inners.models.entities.text_document import TextDocument
from test.mock_data.document_mock_data import DocumentMockData


class TextDocumentMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.document_data = self.document_mock_data.get_data()

    def get_data(self) -> dict:
        return {
            "account": self.document_data["account"],
            "document_type": self.document_data["document_type"],
            "document": self.document_data["document"],
            "text_document": [
                TextDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][0].id,
                    text_content="text_content_1",
                ),
                TextDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][1].id,
                    text_content="text_content_2",
                )
            ]
        }
