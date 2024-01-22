from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.passage_searches.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searches.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.passage_searchs.process_response import ProcessResponse
from app.inners.use_cases.passage_search.passage_search import PassageSearch
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["passage-search"])


@cbv(router)
class PassageSearchController:
    @inject
    def __init__(
            self,
            passage_search: PassageSearch = Depends(
                Provide[ApplicationContainer.use_cases.passage_searches.passage_search]
            )
    ):
        self.passage_search = passage_search

    @router.post("/passage-search")
    async def search(self, body: ProcessBody) -> Content[ProcessResponse]:
        request: ProcessRequest = ProcessRequest(body=body)
        return await self.passage_search.search(request)
