import base64
import uuid
from typing import List, Tuple, Optional, Dict, Any

import more_itertools
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from unstructured.chunking.basic import chunk_elements
from unstructured.documents.elements import Element, Text, NarrativeText, Table, Image
from unstructured.documents.html import HTMLText, HTMLTable

from apps.inners.models.dtos.document_category import DocumentCategory
from apps.inners.models.dtos.element_category import ElementCategory
from apps.inners.use_cases.document_processor.summary_document_processor import SummaryDocumentProcessor


class CategoryDocumentProcessor:
    def __init__(
            self,
            summary_document_processor: SummaryDocumentProcessor,
    ):
        self.summary_document_processor = summary_document_processor

    async def categorize_elements(self, elements: List[Element]) -> ElementCategory:
        categorized_elements: ElementCategory = ElementCategory(
            texts=[],
            tables=[],
            images=[]
        )

        for element in elements:
            if any(
                    element_type == element.__class__.__name__ for element_type in
                    [Text.__name__, NarrativeText.__name__, HTMLText.__name__]

            ):
                categorized_elements.texts.append(element)
            elif any(
                    element_type == element.__class__.__name__ for element_type in
                    [Table.__name__, HTMLTable.__name__]
            ):
                categorized_elements.tables.append(element)
            elif any(
                    element_type == element.__class__.__name__ for element_type in
                    [Image.__name__]
            ):
                file_io = open(element.metadata.image_path, "rb")
                element.metadata.image_mime_type = "image/jpeg"
                element.metadata.image_base64 = base64.b64encode(file_io.read()).decode()
                file_io.close()
                categorized_elements.images.append(element)
            else:
                print(f"BaseDocumentProcessor.categorize_elements: Ignoring element type {element.__class__.__name__}.")

        return categorized_elements

    async def get_categorized_documents(
            self,
            categorized_elements: ElementCategory,
            summarization_model: BaseChatModel,
            is_include_tables: bool = False,
            is_include_images: bool = False,
            chunk_size: int = 400,
            overlap_size: int = 50,
            separators: Tuple[str] = ("\n", " "),
            id_key: str = "id",
            metadata: Optional[Dict[str, Any]] = None,
    ) -> DocumentCategory:
        if metadata is None:
            metadata = {}

        document_category: DocumentCategory = DocumentCategory(
            texts=[],
            tables=[],
            images=[],
            id_key=id_key
        )
        chunked_texts: List[Element] = chunk_elements(
            elements=categorized_elements.texts,
            include_orig_elements=True,
            max_characters=chunk_size - overlap_size,
        )
        if len(chunked_texts) < 2:
            for text in chunked_texts:
                orig_elements: List[Element] = text.metadata.orig_elements
                orig_element_metadata: List[Dict[str, Any]] = [
                    orig_element.metadata.to_dict() for orig_element in orig_elements
                ]
                document: Document = Document(
                    page_content=text.text,
                    metadata={
                        id_key: str(uuid.uuid4()),
                        "category": "text",
                        "orig_metadata": orig_element_metadata,
                        **metadata
                    }
                )
                document_category.texts.append(document)
        else:
            for text_before, text_after in more_itertools.windowed(chunked_texts, n=2):
                orig_elements: List[Element] = []
                for orig_element in text_before.metadata.orig_elements + text_after.metadata.orig_elements:
                    if not any(orig_element.id == existing_orig_element.id for existing_orig_element in orig_elements):
                        orig_elements.append(orig_element)
                orig_elements_metadata: Dict[str, Any] = {
                    "orig_metadata": [
                        orig_element.metadata.to_dict() for orig_element in orig_elements
                    ],
                    "category": "text"
                }
                last_index_of_separators: int = -1
                for separator in separators:
                    last_index_of_separator = text_before.text.rfind(separator, 0, len(text_before.text) - chunk_size)
                    last_index_of_separators = max(last_index_of_separators, last_index_of_separator)

                text = text_before.text[last_index_of_separators + 1:] + " " + text_after.text
                document: Document = Document(
                    page_content=text,
                    metadata={
                        id_key: str(uuid.uuid4()),
                        **orig_elements_metadata,
                        **metadata,
                    }
                )
                document_category.texts.append(document)

        if is_include_tables:
            summarized_tables: List[str] = await self.summary_document_processor.summarize_tables(
                tables=categorized_elements.tables,
                llm_model=summarization_model
            )
            for table, summarized_table in zip(categorized_elements.tables, summarized_tables, strict=True):
                document: Document = Document(
                    page_content=summarized_table,
                    metadata={
                        id_key: str(uuid.uuid4()),
                        "category": "table",
                        **table.metadata.to_dict(),
                        **metadata
                    }
                )
                document_category.tables.append(document)

        if is_include_images:
            summarized_images: List[str] = await self.summary_document_processor.summarize_images(
                images=categorized_elements.images,
                llm_model=summarization_model
            )
            for image, summarized_image in zip(categorized_elements.images, summarized_images, strict=True):
                document: Document = Document(
                    page_content=summarized_image,
                    metadata={
                        id_key: str(uuid.uuid4()),
                        "category": "image",
                        **image.metadata.to_dict(),
                        **metadata
                    }
                )
                document_category.images.append(document)

        return document_category
