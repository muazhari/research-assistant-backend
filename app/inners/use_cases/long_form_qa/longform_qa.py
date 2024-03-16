from app.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from app.inners.models.dtos.contracts.result import Result


class LongFormQA:
    def __init__(
            self,
    ):
        pass

    async def process(self, session: str, body: ProcessBody) -> Result[ProcessResponse]:
        pass
