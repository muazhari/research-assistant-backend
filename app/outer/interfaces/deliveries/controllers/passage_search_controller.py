from datetime import datetime, timedelta

from fastapi import APIRouter

from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.entities.web_document import WebDocument
from app.inner.usecases.passage_search.in_file_search import in_file_search
from app.inner.usecases.passage_search.in_text_search import in_text_search
from app.inner.usecases.passage_search.in_web_search import in_web_search
from app.outer.interfaces.deliveries.contracts.requests.document_search.document_search_request import \
    DocumentSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import \
    DocumentSearchResponse

router = APIRouter(
    prefix="/documents/searches/passages",
    tags=["/documents/searches/passages"]
)


@router.post(path="/text", response_model=Content[DocumentSearchResponse[TextDocument]])
async def passage_search_text(request: DocumentSearchRequest) -> Content[DocumentSearchResponse[TextDocument]]:
    time_start: datetime = datetime.now()
    document_search_response: DocumentSearchResponse[TextDocument] = in_text_search.search(request)
    time_finish: datetime = datetime.now()
    time_delta: timedelta = time_finish - time_start
    document_search_response.process_duration = time_delta.total_seconds()
    content: Content[DocumentSearchResponse] = Content[DocumentSearchResponse](
        message="Passage search text succeed.",
        data=document_search_response
    )
    return content


@router.post(path="/web", response_model=Content[DocumentSearchResponse[WebDocument]])
async def passage_search_web(request: DocumentSearchRequest) -> Content[DocumentSearchResponse[WebDocument]]:
    time_start: datetime = datetime.now()
    document_search_response: DocumentSearchResponse[WebDocument] = in_web_search.search(request)
    time_finish: datetime = datetime.now()
    time_delta: timedelta = time_finish - time_start
    document_search_response.process_duration = time_delta.total_seconds()
    content: Content[DocumentSearchResponse] = Content[DocumentSearchResponse](
        message="Passage search text succeed.",
        data=document_search_response
    )
    return content


@router.post(path="/file", response_model=Content[DocumentSearchResponse[FileDocument]])
async def passage_search_file(request: DocumentSearchRequest) -> Content[DocumentSearchResponse]:
    time_start: datetime = datetime.now()
    document_search_response: DocumentSearchResponse[FileDocument] = in_file_search.search(request)
    time_finish: datetime = datetime.now()
    time_delta: timedelta = time_finish - time_start
    document_search_response.process_duration = time_delta.total_seconds()
    content: Content[DocumentSearchResponse] = Content[DocumentSearchResponse](
        message="Passage search text succeed.",
        data=document_search_response
    )
    return content
