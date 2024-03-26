import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from apps.inners.models.daos.document_process import DocumentProcess
from tests.mocks.document_mock import DocumentMock


class DocumentProcessMock:

    def __init__(
            self,
            document_mock: DocumentMock
    ):
        self.document_mock: DocumentMock = document_mock
        current_time: datetime = datetime.now(tz=timezone.utc)
        started_at: datetime = current_time + timedelta(minutes=0)
        finished_at: datetime = current_time + timedelta(minutes=1)
        self._data: List[DocumentProcess] = [
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_mock.data[0].id,
                final_document_id=self.document_mock.data[1].id,
                started_at=started_at,
                finished_at=finished_at
            ),
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_mock.data[3].id,
                final_document_id=self.document_mock.data[4].id,
                started_at=started_at,
                finished_at=finished_at
            ),
        ]

    @property
    def data(self) -> List[DocumentProcess]:
        return [DocumentProcess(**document_process.dict()) for document_process in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for document_process in self._data:
            if document_process.id == id:
                is_found = True
                self._data.remove(document_process)

        if not is_found:
            raise ValueError(f"DocumentProcess with id {id} is not found.")
