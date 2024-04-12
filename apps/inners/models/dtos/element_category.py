from typing import List, Union

from unstructured.documents.elements import Text, Table, Image, NarrativeText
from unstructured.documents.html import HTMLText, HTMLTable

from apps.inners.models.base_model import BaseModelV2


class ElementCategory(BaseModelV2):
    texts: List[Union[Text, NarrativeText, HTMLText]]
    tables: List[Union[Table, HTMLTable]]
    images: List[Image]

    def to_dict(self):
        return {
            "texts": [text.to_dict() for text in self.texts],
            "tables": [table.to_dict() for table in self.tables],
            "images": [image.to_dict() for image in self.images]
        }
