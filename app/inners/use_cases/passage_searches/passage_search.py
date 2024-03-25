from starlette.datastructures import State

from app.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from app.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse
from app.inners.models.dtos.contracts.result import Result


class PassageSearch:

    def __init__(
            self,
    ):
        pass

    async def process(self, state: State, body: ProcessBody) -> Result[ProcessResponse]:
        pass
