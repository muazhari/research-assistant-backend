import uuid
from typing import List

from apps.inners.models.daos.document import Document
from tests.fakes.account_fake import AccountFake
from tests.fakes.document_type_fake import DocumentTypeFake


class DocumentFake:

    def __init__(
            self,
            account_fake: AccountFake,
            document_type_fake_data: DocumentTypeFake
    ):
        self.account_fake: AccountFake = account_fake
        self.document_type_fake: DocumentTypeFake = document_type_fake_data
        self._data: List[Document] = [
            Document(
                id=uuid.uuid4(),
                name="name0",
                description="description0",
                account_id=self.account_fake.data[0].id,  # This is a dict, not a model
                document_type_id=self.document_type_fake.data[0].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name1",
                description="description1",
                account_id=self.account_fake.data[0].id,
                document_type_id=self.document_type_fake.data[1].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name2",
                description="description2",
                account_id=self.account_fake.data[0].id,
                document_type_id=self.document_type_fake.data[2].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name3",
                description="description3",
                account_id=self.account_fake.data[1].id,
                document_type_id=self.document_type_fake.data[0].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name4",
                description="description4",
                account_id=self.account_fake.data[1].id,
                document_type_id=self.document_type_fake.data[1].id,
            ),
            Document(
                id=uuid.uuid4(),
                name="name5",
                description="description5",
                account_id=self.account_fake.data[1].id,
                document_type_id=self.document_type_fake.data[2].id,
            )
        ]

    @property
    def data(self) -> List[Document]:
        return [Document(**document.dict()) for document in self._data]

    def create_one(self, document: Document):
        self._data.append(document)

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for document in self._data:
            if document.id == id:
                is_found = True
                self._data.remove(document)

        if not is_found:
            raise ValueError(f"Document with id {id} is not found.")
