# from uuid import UUID
#
# from app.core.model.entity.text_document import TextDocument
# from app.infrastucture.repository import text_document_repository
#
#
# def find_all() -> [TextDocument]:
#     text_documents: [TextDocument] = text_document_repository.find_all()
#     return text_documents
#
#
# def find_one_by_id(id: UUID) -> TextDocument:
#     found_text_document: TextDocument = text_document_repository.find_one_by_id(id)
#     return found_text_document
#
#
# def create_one(text_document: TextDocument) -> TextDocument:
#     created_text_document = text_document_repository.create_one(text_document)
#     return created_text_document
#
#
# def update_one_by_id(id: UUID, text_document: TextDocument) -> TextDocument:
#     found_text_document: TextDocument = text_document_repository.update_one_by_id(id, text_document)
#     return found_text_document
#
#
# def delete_one_by_id(id: UUID, text_document: TextDocument) -> TextDocument:
#     found_text_document: TextDocument = text_document_repository.delete_one_by_id(id, text_document)
#     return found_text_document
