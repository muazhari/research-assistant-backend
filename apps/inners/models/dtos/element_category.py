from typing import List

from unstructured.documents.elements import Text, Table, Image

from apps.inners.models.base_model import BaseModelV2


class ElementCategory(BaseModelV2):
    texts: List[Text]
    tables: List[Table]
    images: List[Image]

    def to_dict(self):
        return {
            "texts": [text.to_dict() for text in self.texts],
            "tables": [table.to_dict() for table in self.tables],
            "images": [image.to_dict() for image in self.images]
        }
