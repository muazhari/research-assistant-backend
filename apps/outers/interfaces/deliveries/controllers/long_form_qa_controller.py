from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, Content

from apps.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from apps.inners.use_cases.long_form_qas.process_longform_qa import ProcessLongFormQA


class LongFormQaController:

    def __init__(
            self,
            process_long_form_qa: ProcessLongFormQA
    ):
        self.router: APIRouter = APIRouter(
            tags=["long-form-qas"],
            prefix="/long-form-qas"
        )
        self.router.add_api_route(
            path="",
            endpoint=self.search,
            methods=["POST"]
        )
        self.process_long_form_qa = process_long_form_qa

    async def search(self, request: Request, body: ProcessBody) -> Response:
        data: ProcessResponse = await self.process_long_form_qa.process(
            state=request.state,
            body=body
        )
        content: Content[ProcessResponse] = Content[ProcessResponse](
            status_code=status.HTTP_200_OK,
            message=f"{self.__class__.__name__}.{self.search.__name__}: Succeed.",
            data=data
        )

        return content.to_response()
