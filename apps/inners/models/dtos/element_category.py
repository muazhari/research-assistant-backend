from typing import List, Union

from unstructured.documents.elements import Text, Table, Image, NarrativeText

from apps.inners.models.base_model import BaseModel


class ElementCategory(BaseModel):
    texts: List[Union[Text, NarrativeText]]
    tables: List[Union[Table]]
    images: List[Image]

    def to_dict(self):
        return {
            "texts": [text.to_dict() for text in self.texts],
            "tables": [table.to_dict() for table in self.tables],
            "images": [image.to_dict() for image in self.images]
        }
