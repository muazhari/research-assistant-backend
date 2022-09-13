from datetime import datetime

from fastapi import APIRouter

from app.core.usecase.passage_search.search_passage import search_passage_in_text, search_passage_in_web, \
    search_passage_in_file
from app.infrastucture.delivery.contract.request.document_search.document_search_request import \
    DocumentSearchRequest
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import \
    BaseDocumentSearchResponse

router = APIRouter()


@router.post(path="/text", response_model=BaseDocumentSearchResponse)
async def passage_search_text(request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    time_start = datetime.now()
    document_search_response = await search_passage_in_text(request)
    time_finish = datetime.now()
    time_delta = time_finish - time_start
    return document_search_response


@router.post(path="/web", response_model=BaseDocumentSearchResponse)
async def passage_search_web(request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    time_start = datetime.now()
    document_search_response = search_passage_in_web(request)
    time_finish = datetime.now()
    time_delta = time_finish - time_start
    return document_search_response


@router.post(path="/file", response_model=BaseDocumentSearchResponse)
async def passage_search_file(request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    time_start = datetime.now()
    document_search_response = search_passage_in_file(request)
    time_finish = datetime.now()
    time_delta = time_finish - time_start
    return document_search_response
