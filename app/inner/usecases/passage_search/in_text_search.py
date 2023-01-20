import more_itertools
from haystack.document_stores import FAISSDocumentStore, ElasticsearchDocumentStore
from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.schema import Document
from haystack.utils import print_answers
from txtai.embeddings import Embeddings
from txtai.pipeline import Textractor

from app.inner.model.entities.text_document import TextDocument
from app.inner.usecases.document_conversion.file_conversion import convert_to_file
from app.inner.usecases.document_conversion.text_conversion import convert_to_text
from app.inner.usecases.entity_manager.account_manager import account_manager
from app.inner.usecases.entity_manager.document_manager import document_manager
from app.inner.usecases.entity_manager.document_type_manager import document_type_manager
from app.inner.usecases.entity_manager.text_document_manager import text_document_manager
from app.outer.interfaces.deliveries.contracts.requests.document_search.document_search_request import \
    DocumentSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import \
    DocumentSearchResponse


class InTextSearch:
    def search(self, search_request: DocumentSearchRequest) -> DocumentSearchResponse[TextDocument]:
        found_account = account_manager.read_one_by_id(search_request.account_id)
        found_document = document_manager.read_one_by_id(search_request.document_id)
        found_text_document = text_document_manager.read_one_by_document_id(found_document.id)
        found_conversion_document_type = document_type_manager.read_one_by_id(
            search_request.conversion_document_type_id)

        textractor = None
        if (search_request.granularity == "sentence"):
            textractor = Textractor(sentences=True)
        elif (search_request.granularity == "paragraph"):
            textractor = Textractor(paragraphs=True)

        embeddings = Embeddings({"path": search_request.retriever_model})

        textracted_text = textractor(text=found_text_document.text_content)

        documents = [(id, text, None) for id, text in enumerate(textracted_text)]
        windowed_documents = more_itertools.windowed(seq=documents, n=search_request.window_size)

        embeddings.index(documents=windowed_documents)

        result = embeddings.search(query=search_request.query, limit=len(documents))

        response = None
        if found_conversion_document_type.name == 'text':
            response = convert_to_text(search_request, str(result))
        elif found_conversion_document_type.name == 'file':
            response = convert_to_file(search_request, str(result))
        return response


in_text_search = InTextSearch()
