from typing import TypeVar, Generic

from app.outer.interfaces.deliveries.contracts.responses.base_generic_response import BaseGenericResponse

T = TypeVar("T")


class PassageSearchResponse(BaseGenericResponse, Generic[T]):
    processed_document: T
    process_duration: float
