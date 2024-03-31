from typing import List

from unstructured.documents.elements import Text, Table, Image

from apps.inners.models.base_model import BaseModel


class ElementCategory(BaseModel):
    texts: List[Text]
    tables: List[Table]
    images: List[Image]
