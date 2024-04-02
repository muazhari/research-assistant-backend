from typing import List

from unstructured.documents.elements import Text, Table, Image

from apps.inners.models.base_model import BaseModelV2


class ElementCategory(BaseModelV2):
    texts: List[Text]
    tables: List[Table]
    images: List[Image]
