from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.process_response import ProcessResponse
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

    @router.post("/long-form-qa")
    async def search(self, body: ProcessBody) -> Content[ProcessResponse]:
        request: ProcessRequest = ProcessRequest(body=body)
        return await self.long_form_qa.qa(request)
