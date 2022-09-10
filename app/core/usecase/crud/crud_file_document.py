# from uuid import UUID
#
# from app.core.model.entity.file_document import FileDocument
# from app.infrastucture.repository import file_document_repository
#
#
# def find_all() -> [FileDocument]:
#     file_documents: [FileDocument] = file_document_repository.find_all()
#     return file_documents
#
#
# def find_one_by_id(id: UUID) -> FileDocument:
#     found_file_document: FileDocument = file_document_repository.find_one_by_id(id)
#     return found_file_document
#
#
# def create_one(file_document: FileDocument) -> FileDocument:
#     created_file_document = file_document_repository.create_one(file_document)
#     return created_file_document
#
#
# def update_one_by_id(id: UUID, file_document: FileDocument) -> FileDocument:
#     found_file_document: FileDocument = file_document_repository.update_one_by_id(id, file_document)
#     return found_file_document
#
#
# def delete_one_by_id(id: UUID, file_document: FileDocument) -> FileDocument:
#     found_file_document: FileDocument = file_document_repository.delete_one_by_id(id, file_document)
#     return found_file_document
