import uuid

from app.inners.models.entities.document_process import DocumentProcess
from test.mock_data.document_mock_data import DocumentMockData


class DocumentProcessMockData:

    def __init__(self):
        self.document_mock_data = DocumentMockData()
        self.data = [
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_mock_data.data[0].id,
                final_document_id=self.document_mock_data.data[1].id,
                process_duration=0.0,
            ),
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_mock_data.data[1].id,
                final_document_id=self.document_mock_data.data[0].id,
                process_duration=1.0,
            )
        ]
