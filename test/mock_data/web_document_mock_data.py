import uuid

from app.inners.models.entities.web_document import WebDocument
from test.mock_data.document_mock_data import DocumentMockData


class WebDocumentMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.document_data = self.document_mock_data.get_data()

    def get_data(self) -> dict:
        return {
            "account": self.document_data["account"],
            "document_type": self.document_data["document_type"],
            "document": self.document_data["document"],
            "web_document": [
                WebDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][0].id,
                    web_url="web_url_1",
                ),
                WebDocument(
                    id=uuid.uuid4(),
                    document_id=self.document_data["document"][1].id,
                    web_url="web_url_2",
                )
            ]
        }
