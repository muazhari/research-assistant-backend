from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse


class TextDocumentResponse(DocumentResponse, table=True):
    text_content: str
