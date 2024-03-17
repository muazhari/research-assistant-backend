from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import Response

from app.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from app.inners.models.dtos.contracts.result import Result
from app.inners.use_cases.long_form_qa.longform_qa import LongFormQA
from app.outers.containers.application_container import ApplicationContainer

router: APIRouter = APIRouter(tags=["long-form-qa"])


@cbv(router)
class PassageSearchController:

    @inject
    def __init__(
            self,
            long_form_qa: LongFormQA = Depends(
                Provide[ApplicationContainer.use_cases.longform_qas.longform_qa]
            )
    ):
        self.long_form_qa = long_form_qa

    @router.post("/long-form-qas")
    async def search(self, request: Request, body: ProcessBody) -> Response:
        result: Result[ProcessResponse] = await self.long_form_qa.process(
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
