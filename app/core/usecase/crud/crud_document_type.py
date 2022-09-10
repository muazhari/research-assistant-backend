# from uuid import UUID
#
# from app.core.model.entity.document_type import DocumentType
# from app.infrastucture.repository import document_type_repository
#
#
# def find_all() -> [DocumentType]:
#     document_types: [DocumentType] = document_type_repository.find_all()
#     return document_types
#
#
# def find_one_by_id(id: UUID) -> DocumentType:
#     found_document_type: DocumentType = document_type_repository.find_one_by_id(id)
#     return found_document_type
#
#
# def create_one(document_type: DocumentType) -> DocumentType:
#     created_document_type = document_type_repository.create_one(document_type)
#     return created_document_type
#
#
# def update_one_by_id(id: UUID, document_type: DocumentType) -> DocumentType:
#     found_document_type: DocumentType = document_type_repository.update_one_by_id(id, document_type)
#     return found_document_type
#
#
# def delete_one_by_id(id: UUID, document_type: DocumentType) -> DocumentType:
#     found_document_type: DocumentType = document_type_repository.delete_one_by_id(id, document_type)
#     return found_document_type
