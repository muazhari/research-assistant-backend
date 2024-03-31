from starlette.datastructures import State

from apps.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse


class ProcessLongFormQA:
    def __init__(
            self,
    ):
        pass

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        pass
