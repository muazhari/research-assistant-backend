# from uuid import UUID
#
# from app.core.model.entity.web_document import WebDocument
# from app.infrastucture.repository import web_document_repository
#
#
# def find_all() -> [WebDocument]:
#     web_documents: [WebDocument] = web_document_repository.find_all()
#     return web_documents
#
#
# def find_one_by_id(id: UUID) -> WebDocument:
#     found_web_document: WebDocument = web_document_repository.find_one_by_id(id)
#     return found_web_document
#
#
# def create_one(web_document: WebDocument) -> WebDocument:
#     created_web_document = web_document_repository.create_one(web_document)
#     return created_web_document
#
#
# def update_one_by_id(id: UUID, web_document: WebDocument) -> WebDocument:
#     found_web_document: WebDocument = web_document_repository.update_one_by_id(id, web_document)
#     return found_web_document
#
#
# def delete_one_by_id(id: UUID, web_document: WebDocument) -> WebDocument:
#     found_web_document: WebDocument = web_document_repository.delete_one_by_id(id, web_document)
#     return found_web_document
