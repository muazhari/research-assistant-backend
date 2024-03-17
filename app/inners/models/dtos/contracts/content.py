from typing import Generic, TypeVar, Optional

from pydantic.generics import GenericModel

from app.inners.models.dtos.base_dto import BaseDto

T = TypeVar("T")


class Content(BaseDto, GenericModel, Generic[T]):
    message: str
    data: Optional[T]