from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.process_response import ProcessResponse
from app.inners.use_cases.long_form_qa.longform_qa import LongFormQA

router: APIRouter = APIRouter(tags=["long-form-qa"])


@cbv(router)
class PassageSearchController:
    def __init__(self):
        self.long_form_qa = LongFormQA()

    @router.post("/long-form-qa")
    async def search(self, body: ProcessBody) -> Content[ProcessResponse]:
        request: ProcessRequest = ProcessRequest(body=body)
        return await self.long_form_qa.qa(request)
