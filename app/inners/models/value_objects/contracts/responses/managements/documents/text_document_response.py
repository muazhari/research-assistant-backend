from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse


class TextDocumentResponse(DocumentResponse):
    text_content: str
