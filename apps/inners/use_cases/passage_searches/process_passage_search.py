from starlette.datastructures import State

from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse
from apps.inners.use_cases.graphs.passage_search_graph import PassageSearchGraph


class ProcessPassageSearch:

    def __init__(
            self,
            passage_search_graph: PassageSearchGraph,
    ):
        self.passage_search_graph = passage_search_graph

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        pass
