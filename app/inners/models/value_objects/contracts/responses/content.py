from typing import Generic, TypeVar, Optional

from pydantic.generics import GenericModel

from app.inners.models.value_objects.base_value_object import BaseValueObject

T = TypeVar("T")


class Content(BaseValueObject, GenericModel, Generic[T]):
    message: str
    data: Optional[T]
