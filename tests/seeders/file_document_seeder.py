import io

from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.file_document import FileDocument
from apps.outers.datastores.three_datastore import ThreeDatastore
from tests.fakes.file_document_fake import FileDocumentFake


class FileDocumentSeeder:

    def __init__(
            self,
            file_document_fake: FileDocumentFake,
            three_datastore: ThreeDatastore
    ):
        self.file_document_fake: FileDocumentFake = file_document_fake
        self.three_datastore: ThreeDatastore = three_datastore

    async def up(self, session: AsyncSession):
        for index, file_document in enumerate(self.file_document_fake.data):
            self.three_datastore.client.put_object(
                bucket_name="research-assistant-backend.file-documents",
                object_name=file_document.file_name,
                data=io.BytesIO(self.file_document_fake.file_data[index]),
                length=len(self.file_document_fake.file_data[index])
            )
            session.add(file_document)

    async def down(self, session: AsyncSession):
        for index, file_document in enumerate(self.file_document_fake.data):
            found_file_document_result: Result = await session.exec(
                select(FileDocument).where(FileDocument.id == file_document.id).limit(1)
            )
            found_file_document: FileDocument = found_file_document_result.one()
            self.three_datastore.client.remove_object(
                bucket_name="research-assistant-backend.file-documents",
                object_name=found_file_document.file_name
            )
            await session.delete(found_file_document)
