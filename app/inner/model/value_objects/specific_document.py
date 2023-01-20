from typing import TypeVar, Generic

from pydantic.generics import GenericModel

from app.inner.model.entities.document import Document

T = TypeVar("T")


class SpecificDocument(GenericModel, Generic[T]):
    document: Document
    document_detail: T
