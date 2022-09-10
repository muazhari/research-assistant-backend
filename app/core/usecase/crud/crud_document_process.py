# from uuid import UUID
#
# from app.core.model.entity.document_process import DocumentProcess
# from app.infrastucture.repository import document_process_repository
#
#
# def find_all() -> [DocumentProcess]:
#     document_processs: [DocumentProcess] = document_process_repository.find_all()
#     return document_processs
#
#
# def find_one_by_id(id: UUID) -> DocumentProcess:
#     found_document_process: DocumentProcess = document_process_repository.find_one_by_id(id)
#     return found_document_process
#
#
# def create_one(document_process: DocumentProcess) -> DocumentProcess:
#     created_document_process = document_process_repository.create_one(document_process)
#     return created_document_process
#
#
# def update_one_by_id(id: UUID, document_process: DocumentProcess) -> DocumentProcess:
#     found_document_process: DocumentProcess = document_process_repository.update_one_by_id(id, document_process)
#     return found_document_process
#
#
# def delete_one_by_id(id: UUID, document_process: DocumentProcess) -> DocumentProcess:
#     found_document_process: DocumentProcess = document_process_repository.delete_one_by_id(id, document_process)
#     return found_document_process
