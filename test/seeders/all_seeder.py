import asyncpg
import sqlalchemy.exc
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
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            session = await self.one_datastore.get_session()
            try:
                await session.begin()
                await self.account_seeder.up(session)
                # await self.document_type_seeder.up(session)
                await self.document_seeder.up(session)
                await self.document_process_seeder.up(session)
                await self.text_document_seeder.up(session)
                await self.file_document_seeder.up(session)
                await self.web_document_seeder.up(session)
                await session.commit()
                break
            except sqlalchemy.exc.DBAPIError as exception:
                if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                    retry_count += 1
                    continue
                raise exception
            except Exception as exception:
                await session.rollback()
                raise exception

        if retry_count == max_retries:
            raise Exception("AllSeeder.up: Retry count is equal to max retries.")

    async def down(self):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            session: AsyncSession = await self.one_datastore.get_session()
            try:
                await session.begin()
                await self.web_document_seeder.down(session)
                await self.file_document_seeder.down(session)
                await self.text_document_seeder.down(session)
                await self.document_process_seeder.down(session)
                await self.document_seeder.down(session)
                # await self.document_type_seeder.up(session)
                await self.account_seeder.down(session)
                await session.commit()
                break
            except sqlalchemy.exc.DBAPIError as exception:
                if exception.orig.pgcode == asyncpg.exceptions.SerializationError.sqlstate:
                    retry_count += 1
                    continue
                raise exception
            except Exception as exception:
                await session.rollback()
                raise exception

        if retry_count == max_retries:
            raise Exception("AllSeeder.down: Retry count is equal to max retries.")
