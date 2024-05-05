from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document import Document
from apps.outers.datastores.one_datastore import OneDatastore
from tests.seeders.account_seeder import AccountSeeder
from tests.seeders.document_process_seeder import DocumentProcessSeeder
from tests.seeders.document_seeder import DocumentSeeder
from tests.seeders.document_type_seeder import DocumentTypeSeeder
from tests.seeders.file_document_seeder import FileDocumentSeeder
from tests.seeders.session_seeder import SessionSeeder
from tests.seeders.text_document_seeder import TextDocumentSeeder
from tests.seeders.web_document_seeder import WebDocumentSeeder


class AllSeeder:
    def __init__(
            self,
            one_datastore: OneDatastore,
            account_seeder: AccountSeeder,
            session_seeder: SessionSeeder,
            document_type_seeder: DocumentTypeSeeder,
            document_seeder: DocumentSeeder,
            document_process_seeder: DocumentProcessSeeder,
            text_document_seeder: TextDocumentSeeder,
            file_document_seeder: FileDocumentSeeder,
            web_document_seeder: WebDocumentSeeder,
    ):
        self.one_datastore: OneDatastore = one_datastore
        self.account_seeder: AccountSeeder = account_seeder
        self.session_seeder: SessionSeeder = session_seeder
        self.document_type_seeder: DocumentTypeSeeder = document_type_seeder
        self.document_seeder: DocumentSeeder = document_seeder
        self.document_process_seeder: DocumentProcessSeeder = document_process_seeder
        self.text_document_seeder: TextDocumentSeeder = text_document_seeder
        self.file_document_seeder: FileDocumentSeeder = file_document_seeder
        self.web_document_seeder: WebDocumentSeeder = web_document_seeder

    async def up(self):
        async def handler(session: AsyncSession):
            await self.account_seeder.up(session)
            await self.session_seeder.up(session)
            # await self.document_type_seeder.up(session)
            await self.document_seeder.up(session)
            await self.document_process_seeder.up(session)
            await self.text_document_seeder.up(session)
            await self.file_document_seeder.up(session)
            await self.web_document_seeder.up(session)
            return

        await self.one_datastore.retryable(handler)

    async def down(self):
        async def handler(session: AsyncSession):
            await self.web_document_seeder.down(session)
            await self.file_document_seeder.down(session)
            await self.text_document_seeder.down(session)
            await self.document_process_seeder.down(session)
            await self.document_seeder.down(session)
            # await self.document_type_seeder.down(session)
            await self.session_seeder.down(session)
            await self.account_seeder.down(session)

        await self.one_datastore.retryable(handler)

    async def up_one_document(self, document: Document):
        self.document_seeder.document_fake.create_one(document)

        async def handler(session: AsyncSession):
            session.add(Document(**document.model_dump()))

        await self.one_datastore.retryable(handler)

    def delete_many_web_document_by_id_cascade(self, id: UUID):
        self.web_document_seeder.web_document_fake.delete_many_by_id(id)
        self.delete_many_document_by_id_cascade(id)

    def delete_many_file_document_by_id_cascade(self, id: UUID):
        self.file_document_seeder.file_document_fake.delete_many_by_id(id)
        self.delete_many_document_by_id_cascade(id)

    def delete_many_text_document_by_id_cascade(self, id: UUID):
        self.text_document_seeder.text_document_fake.delete_many_by_id(id)
        self.delete_many_document_by_id_cascade(id)

    def delete_many_document_process_by_id_cascade(self, id: UUID):
        self.document_process_seeder.document_process_fake.delete_many_by_id(id)

    def delete_many_document_by_id_cascade(self, id: UUID):
        for web_document in self.web_document_seeder.web_document_fake.data:
            if id in [web_document.id]:
                self.web_document_seeder.web_document_fake.delete_many_by_id(id)

        for file_document in self.file_document_seeder.file_document_fake.data:
            if id in [file_document.id]:
                self.file_document_seeder.file_document_fake.delete_many_by_id(id)

        for text_document in self.text_document_seeder.text_document_fake.data:
            if id in [text_document.id]:
                self.text_document_seeder.text_document_fake.delete_many_by_id(id)

        for document_process in self.document_process_seeder.document_process_fake.data:
            if id in [document_process.initial_document_id, document_process.final_document_id]:
                self.document_process_seeder.document_process_fake.delete_many_by_id(document_process.id)

        self.document_seeder.document_fake.delete_many_by_id(id)

    def delete_many_account_by_id_cascade(self, id: UUID):
        for document in self.document_seeder.document_fake.data:
            if id in [document.account_id]:
                self.delete_many_document_by_id_cascade(document.id)

        for session in self.session_seeder.session_fake.data:
            if id in [session.account_id]:
                self.session_seeder.session_fake.delete_many_by_id(session.id)

        self.account_seeder.account_fake.delete_many_by_id(id)

    def delete_many_session_by_id_cascade(self, id: UUID):
        self.session_seeder.session_fake.delete_many_by_id(id)
