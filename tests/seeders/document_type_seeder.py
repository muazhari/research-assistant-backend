from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document_type import DocumentType
from tests.fakes.document_type_fake import DocumentTypeFake


class DocumentTypeSeeder:

    def __init__(
            self,
            document_type_fake: DocumentTypeFake
    ):
        self.document_type_fake: DocumentTypeFake = document_type_fake

    async def up(self, session: AsyncSession):
        for document_type in self.document_type_fake.data:
            session.add(document_type)

    async def down(self, session: AsyncSession):
        for document_type in self.document_type_fake.data:
            found_document_type_result: Result = await session.exec(
                select(DocumentType).where(DocumentType.id == document_type.id).limit(1)
            )
            found_document_type: DocumentType = found_document_type_result.one()
            await session.delete(found_document_type)
