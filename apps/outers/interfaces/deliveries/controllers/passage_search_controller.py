from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, Content

from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse
from apps.inners.use_cases.passage_searches.process_passage_search import ProcessPassageSearch


class PassageSearchController:

    def __init__(
            self,
            process_passage_search: ProcessPassageSearch
    ):
        self.router: APIRouter = APIRouter(
            tags=["passage-searches"],
            prefix="/passage-searches"
        )
        self.router.add_api_route(
            path="",
            endpoint=self.search,
            methods=["POST"]
        )
        self.process_passage_search = process_passage_search

    async def search(self, request: Request, body: ProcessBody) -> Response:
        data: ProcessResponse = await self.process_passage_search.process(
            state=request.state,
            body=body
        )
        content: Content[ProcessResponse] = Content[ProcessResponse](
            status_code=status.HTTP_200_OK,
            message=f"{self.__class__.__name__}.{self.search.__name__}: Succeed.",
            data=data
        )

        return content.to_response()
