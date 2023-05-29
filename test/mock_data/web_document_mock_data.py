import uuid
from typing import List

from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from test.mock_data.document_mock_data import DocumentMockData


class WebDocumentMockData:

    def __init__(self):
        self.document_mock_data: DocumentMockData = DocumentMockData()
        self.data: List[WebDocument] = [
            WebDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[0].id,
                web_url="web_url_0",
            ),
            WebDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[1].id,
                web_url="web_url_1",
            )
        ]
        self.response_data: List[WebDocumentResponse] = [
            WebDocumentResponse(
                id=self.document_mock_data.data[0].id,
                name=self.document_mock_data.data[0].name,
                description=self.document_mock_data.data[0].description,
                document_type_id=self.document_mock_data.data[0].document_type_id,
                account_id=self.document_mock_data.data[0].account_id,
                web_url=self.data[0].web_url,
            ),
            WebDocumentResponse(
                id=self.document_mock_data.data[1].id,
                name=self.document_mock_data.data[1].name,
                description=self.document_mock_data.data[1].description,
                document_type_id=self.document_mock_data.data[1].document_type_id,
                account_id=self.document_mock_data.data[1].account_id,
                web_url=self.data[1].web_url,
            )
        ]
