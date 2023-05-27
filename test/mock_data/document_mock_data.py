import uuid

from app.inners.models.entities.document import Document
from test.mock_data.account_mock_data import AccountMockData
from test.mock_data.document_type_mock_data import DocumentTypeMockData


class DocumentMockData:

    def __init__(self):
        self.account_mock_data = AccountMockData()
        self.account_data = self.account_mock_data.get_data()
        self.document_type_mock_data = DocumentTypeMockData()
        self.document_type_data = self.document_type_mock_data.get_data()

    def get_data(self) -> dict:
        return {
            "account": self.account_data["account"],
            "document_type": self.document_type_data["document_type"],
            "document": [
                Document(
                    id=uuid.uuid4(),
                    name="name0",
                    description="description0",
                    account_id=self.account_data["account"][0].id,
                    document_type_id=self.document_type_data["document_type"][0].id,
                ),
                Document(
                    id=uuid.uuid4(),
                    name="name1",
                    description="description1",
                    account_id=self.account_data["account"][1].id,
                    document_type_id=self.document_type_data["document_type"][1].id,
                )
            ]

        }
