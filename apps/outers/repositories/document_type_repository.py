import sqlalchemy.exc
from sqlalchemy.engine import ScalarResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.inners.exceptions import repository_exception
from apps.inners.models.daos.document_type import DocumentType


class DocumentTypeRepository:

    def __init__(self):
        pass

    async def find_one_by_id(self, session: AsyncSession, id: str) -> DocumentType:
        try:
            found_document_type_result: ScalarResult = await session.exec(
                select(DocumentType).where(DocumentType.id == id).limit(1)
            )
            found_document_type: DocumentType = found_document_type_result.one()
        except sqlalchemy.exc.NoResultFound:
            raise repository_exception.NotFound()

        return found_document_type

    async def patch_one_by_id(self, session: AsyncSession, id: str,
                              document_type_patcher: DocumentType) -> DocumentType:
        found_document_type: DocumentType = await self.find_one_by_id(
            session=session,
            id=id
        )
        found_document_type.patch_from(document_type_patcher.dict(exclude_none=True))
        return found_document_type
