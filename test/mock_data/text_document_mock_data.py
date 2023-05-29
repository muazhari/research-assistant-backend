import uuid

from app.inners.models.entities.text_document import TextDocument
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from test.mock_data.document_mock_data import DocumentMockData


class TextDocumentMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.data = [
            TextDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[0].id,
                text_content="text_content_0",
            ),
            TextDocument(
                id=uuid.uuid4(),
                document_id=self.document_mock_data.data[1].id,
                text_content="text_content_1",
            )
        ],
        self.response_data = [
            TextDocumentResponse(
                id=self.document_mock_data.data[0].id,
                name=self.document_mock_data.data[0].name,
                description=self.document_mock_data.data[0].description,
                document_type_id=self.document_mock_data.data[0].document_type_id,
                account_id=self.document_mock_data.data[0].account_id,
                text_content=self.data[0].text_content,
            ),
            TextDocumentResponse(
                id=self.document_mock_data.data[1].id,
                name=self.document_mock_data.data[1].name,
                description=self.document_mock_data.data[1].description,
                document_type_id=self.document_mock_data.data[1].document_type_id,
                account_id=self.document_mock_data.data[1].account_id,
                text_content=self.data[1].text_content,
            )
        ]
