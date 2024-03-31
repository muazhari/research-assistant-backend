from starlette.datastructures import State

from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse


class PassageSearch:

    def __init__(
            self,
    ):
        pass

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        pass
