from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.passage_search.process_response import ProcessResponse
from app.inners.use_cases.passage_search.passage_search import PassageSearch

router: APIRouter = APIRouter(tags=["passage-search"])


@cbv(router)
class PassageSearchController:
    def __init__(self):
        self.passage_search = PassageSearch()

    @router.post("/passage-search")
    async def search(self, body: ProcessBody) -> Content[ProcessResponse]:
        request: ProcessRequest = ProcessRequest(body=body)
        return await self.passage_search.search(request)
