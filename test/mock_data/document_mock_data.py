import uuid
from typing import List

from app.inners.models.entities.document import Document
from test.mock_data.account_mock_data import AccountMockData
from test.mock_data.document_type_mock_data import DocumentTypeMockData


class DocumentMockData:

    def __init__(self):
        self.account_mock_data: AccountMockData = AccountMockData()
        self.document_type_mock_data: DocumentTypeMockData = DocumentTypeMockData()
        self.data: List[Document] = [
            Document(
                id=uuid.uuid4(),
                name="name0",
                description="description0",
                account_id=self.account_mock_data.data[0].id,
                document_type_id=self.document_type_mock_data.data[0].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name1",
                description="description1",
                account_id=self.account_mock_data.data[1].id,
                document_type_id=self.document_type_mock_data.data[1].id,
            )
        ]
