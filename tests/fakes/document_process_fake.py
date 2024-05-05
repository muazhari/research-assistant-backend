import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from apps.inners.models.daos.document_process import DocumentProcess
from tests.fakes.document_fake import DocumentFake


class DocumentProcessFake:

    def __init__(
            self,
            document_fake: DocumentFake
    ):
        self.document_fake: DocumentFake = document_fake
        current_time: datetime = datetime.now(tz=timezone.utc)
        started_at: datetime = current_time + timedelta(minutes=0)
        finished_at: datetime = current_time + timedelta(minutes=1)
        self._data: List[DocumentProcess] = [
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_fake.data[0].id,
                final_document_id=self.document_fake.data[1].id,
                started_at=started_at,
                finished_at=finished_at
            ),
            DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=self.document_fake.data[3].id,
                final_document_id=self.document_fake.data[4].id,
                started_at=started_at,
                finished_at=finished_at
            ),
        ]

    @property
    def data(self) -> List[DocumentProcess]:
        return [DocumentProcess(**document_process.model_dump()) for document_process in self._data]

    def delete_many_by_id(self, id: uuid.UUID):
        is_found: bool = False
        for document_process in self._data:
            if document_process.id == id:
                is_found = True
                self._data.remove(document_process)

        if not is_found:
            raise ValueError(f"DocumentProcess with id {id} is not found.")
