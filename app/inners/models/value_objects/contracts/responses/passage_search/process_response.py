from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse


class ProcessResponse(BaseResponse):
    retrieval_result: dict
    process_duration: float
