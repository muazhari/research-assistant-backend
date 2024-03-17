from sqlmodel.ext.asyncio.session import AsyncSession

from app.outers.datastores.one_datastore import OneDatastore
from test.seeders.account_seeder import AccountSeeder
from test.seeders.document_process_seeder import DocumentProcessSeeder
from test.seeders.document_seeder import DocumentSeeder
from test.seeders.document_type_seeder import DocumentTypeSeeder
from test.seeders.file_document_seeder import FileDocumentSeeder
from test.seeders.text_document_seeder import TextDocumentSeeder
from test.seeders.web_document_seeder import WebDocumentSeeder


class AllSeeder:
    def __init__(
            self,
            one_datastore: OneDatastore,
            account_seeder: AccountSeeder,
            document_type_seeder: DocumentTypeSeeder,
            document_seeder: DocumentSeeder,
            document_process_seeder: DocumentProcessSeeder,
            text_document_seeder: TextDocumentSeeder,
            file_document_seeder: FileDocumentSeeder,
            web_document_seeder: WebDocumentSeeder,
    ):
        self.one_datastore: OneDatastore = one_datastore
        self.account_seeder: AccountSeeder = account_seeder
        self.document_type_seeder: DocumentTypeSeeder = document_type_seeder
        self.document_seeder: DocumentSeeder = document_seeder
        self.document_process_seeder: DocumentProcessSeeder = document_process_seeder
        self.text_document_seeder: TextDocumentSeeder = text_document_seeder
        self.file_document_seeder: FileDocumentSeeder = file_document_seeder
        self.web_document_seeder: WebDocumentSeeder = web_document_seeder

    async def up(self):
        async def handler(session: AsyncSession):
            await self.account_seeder.up(session)
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
            await self.account_seeder.down(session)

        await self.one_datastore.retryable(handler)
