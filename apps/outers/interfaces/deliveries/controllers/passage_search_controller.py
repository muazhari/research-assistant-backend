from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.passage_searches.passage_search import PassageSearch
from apps.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["long-form-qa"])


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

    @router.post("/passage-searches")
    async def search(self, request: Request, body: ProcessBody) -> Response:
        result: Result[ProcessResponse] = await self.passage_search.process(
            state=request.state,
            body=body
        )
        response: Response = Response(
            status_code=result.status_code,
            content=ProcessResponse(
                message=result.message,
                data=result.data
            )
        )
        return response
