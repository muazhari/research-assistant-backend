import uuid

from app.inners.models.entities.document_type import DocumentType


class DocumentTypeMockData:

    def __init__(self):
        self.data = [
            DocumentType(
                id=uuid.uuid4(),
                name="name0",
                description="description0",
            ),
            DocumentType(
                id=uuid.uuid4(),
                name="name1",
                description="description1",
            )
        ]
