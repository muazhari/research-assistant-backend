from starlette.datastructures import State

from apps.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from apps.inners.use_cases.graphs.long_form_qa_graph import LongFormQaGraph


class ProcessLongFormQa:
    def __init__(
            self,
            long_form_qa_graph: LongFormQaGraph,
    ):
        self.long_form_qa_graph = long_form_qa_graph

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        pass
