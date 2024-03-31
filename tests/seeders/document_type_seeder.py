from sqlalchemy.engine import Result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.models.daos.document_type import DocumentType
from tests.mocks.document_type_mock import DocumentTypeMock


class DocumentTypeSeeder:

    def __init__(
            self,
            document_type_mock: DocumentTypeMock
    ):
        self.document_type_mock: DocumentTypeMock = document_type_mock

    async def up(self, session: AsyncSession):
        for document_type in self.document_type_mock.data:
            session.add(document_type)

    async def down(self, session: AsyncSession):
        for document_type in self.document_type_mock.data:
            found_document_type_result: Result = await session.execute(
                select(DocumentType).where(DocumentType.id == document_type.id).limit(1)
            )
            found_document_type: DocumentType = found_document_type_result.scalars().one()
            await session.delete(found_document_type)
