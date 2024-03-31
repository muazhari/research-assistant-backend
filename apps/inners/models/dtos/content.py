from typing import Generic, TypeVar, Optional

from pydantic.generics import GenericModel
from starlette.responses import Response

from apps.inners.models.dtos.base_dto import BaseDto

T = TypeVar("T")


class Content(BaseDto, GenericModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T]

    def to_response(self) -> Response:
        return Response(
            status_code=self.status_code,
            content=self.json(exclude={"status_code"})
        )
