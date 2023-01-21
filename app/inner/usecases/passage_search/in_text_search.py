import uuid
from datetime import datetime, timedelta
from typing import Any

from haystack.document_stores import PineconeDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.schema import Document

from app.inner.model.entities.document_type import DocumentType
from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.value_objects.passage_search.text_passage_search_result import TextPassageSearchResult
from app.inner.model.value_objects.specific_document import SpecificDocument
from app.inner.usecases.document_conversion.document_conversion import document_conversion
from app.inner.usecases.entity_manager.document_manager import document_manager
from app.inner.usecases.entity_manager.document_type_manager import document_type_manager
from app.inner.usecases.entity_manager.text_document_manager import text_document_manager
from app.inner.usecases.passage_search.pre_processor import pre_processor
from app.outer.interfaces.deliveries.contracts.requests.passage_search.passage_search_request import \
    PassageSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content
from app.outer.interfaces.deliveries.contracts.responses.passage_search.passage_search_response import \
    PassageSearchResponse
from app.outer.settings.document_store_settings import document_store_settings
from app.outer.settings.retriever_settings import retriever_settings
from app.outer.utility.java_bytes import b64_encode


class InTextSearch:
    def search(self, passage_search_request: PassageSearchRequest) -> PassageSearchResponse[TextDocument]:
        time_start: datetime = datetime.now()
        found_document: Content[Document] = document_manager.read_one_by_id(passage_search_request.document_id)
        found_text_document: Content[TextDocument] = text_document_manager.read_one_by_document_id(
            found_document.data.id)
        found_conversion_document_type: Content[DocumentType] = document_type_manager.read_one_by_id(
            passage_search_request.conversion_document_type_id)

        document_store = PineconeDocumentStore(
            api_key=document_store_settings.DOCUMENT_STORE_PINECONE_API_KEY,
            index="semantic-search",
            environment="us-west1-gcp",
            similarity="cosine",
            embedding_dim=1024,
            return_embedding=True
        )

        retriever = EmbeddingRetriever(
            document_store=document_store,
            model_format="openai",
            embedding_model=passage_search_request.retriever_model,
            api_key=retriever_settings.RETRIEVER_OPEN_AI_API_KEY,
        )

        pre_processed_corpus = pre_processor.process(
            corpus=found_text_document.data.text_content,
            source_type="text",
            granularity=passage_search_request.granularity,
            window_size=passage_search_request.window_size
        )

        documents = []
        for index_window, window in enumerate(pre_processed_corpus):
            document = Document(
                content=pre_processor.degranularize(
                    corpus=window,
                    granularity_source=passage_search_request.granularity
                ),
                meta={"index_window": index_window}
            )
            documents.append(document)

        pipeline_retrieval = DocumentSearchPipeline(retriever)

        document_store.write_documents(documents)
        document_store.update_embeddings(retriever)

        retrieval_result = pipeline_retrieval.run(
            query=passage_search_request.query,
            params={"Retriever": {"top_k": len(documents)}}
        )

        time_finish: datetime = datetime.now()

        time_delta: timedelta = time_finish - time_start

        response: Any = None
        if found_conversion_document_type.data.name == 'text':
            text_passage_search_result: TextPassageSearchResult = TextPassageSearchResult(
                retrieval_result=retrieval_result,
                text_content=str(retrieval_result["documents"]),
            )
            text_specific_document: SpecificDocument[TextDocument] = document_conversion.create_text_document(
                passage_search_request=passage_search_request,
                text_passage_search_result=text_passage_search_result,
            )
            response: PassageSearchResponse[SpecificDocument[TextDocument]] = PassageSearchResponse(
                processed_document=text_specific_document,
                process_duration=time_delta.total_seconds()
            )
        elif found_conversion_document_type.data.name == 'file':
            file_passage_search_result: TextPassageSearchResult = TextPassageSearchResult(
                retrieval_result=retrieval_result,
                file_bytes=b64_encode(str(retrieval_result["documents"])),
                file_name=uuid.uuid4(),
                file_extension="txt"
            )
            file_specific_document: SpecificDocument[FileDocument] = document_conversion.create_file_document(
                passage_search_request=passage_search_request,
                in_file_passage_search_result=file_passage_search_result,
            )
            response: PassageSearchResponse[SpecificDocument[FileDocument]] = PassageSearchResponse(
                processed_document=file_specific_document,
                process_duration=time_delta.total_seconds()
            )
        return response


in_text_search = InTextSearch()
