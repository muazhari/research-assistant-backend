from fastapi import APIRouter

from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.entities.web_document import WebDocument
from app.inner.model.value_objects.specific_document import SpecificDocument
from app.inner.usecases.passage_search.in_file_search import in_file_search
from app.inner.usecases.passage_search.in_text_search import in_text_search
from app.inner.usecases.passage_search.in_web_search import in_web_search
from app.outer.interfaces.deliveries.contracts.requests.passage_search.passage_search_request import \
    PassageSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.interfaces.deliveries.contracts.responses.passage_search.passage_search_response import \
    PassageSearchResponse

router = APIRouter(
    prefix="/documents/searches/passages",
    tags=["/documents/searches/passages"]
)


@router.post(path="/text", response_model=Content[PassageSearchResponse[SpecificDocument[TextDocument]]])
async def passage_search_text(passage_search_request: PassageSearchRequest) \
        -> Content[PassageSearchResponse[SpecificDocument[TextDocument]]]:
    passage_search_response: PassageSearchResponse[SpecificDocument[TextDocument]] = in_text_search.search(
        passage_search_request)
    content: Content[PassageSearchResponse[SpecificDocument[TextDocument]]] = \
        Content[PassageSearchResponse[SpecificDocument[TextDocument]]](
            message="Passage search in text succeed.",
            data=passage_search_response
        )
    return content


@router.post(path="/web", response_model=Content[PassageSearchResponse[SpecificDocument[WebDocument]]])
async def passage_search_web(request: PassageSearchRequest) \
        -> Content[PassageSearchResponse[SpecificDocument[WebDocument]]]:
    passage_search_response: PassageSearchResponse[SpecificDocument[WebDocument]] = in_web_search.search(request)
    content: Content[PassageSearchResponse[SpecificDocument[WebDocument]]] = \
        Content[PassageSearchResponse[SpecificDocument[WebDocument]]](
            message="Passage search in web succeed.",
            data=passage_search_response
        )
    return content


@router.post(path="/file", response_model=Content[PassageSearchResponse[SpecificDocument[FileDocument]]])
async def passage_search_file(request: PassageSearchRequest) \
        -> Content[PassageSearchResponse]:
    passage_search_response: PassageSearchResponse[SpecificDocument[FileDocument]] = in_file_search.search(request)
    content: Content[PassageSearchResponse[SpecificDocument[FileDocument]]] = \
        Content[PassageSearchResponse[SpecificDocument[FileDocument]]](
            message="Passage search in file succeed.",
            data=passage_search_response
        )
    return content
