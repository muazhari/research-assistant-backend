import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import BaseRetriever, JoinDocuments, BaseRanker
from haystack.schema import Document as DocumentHaystack

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentTypeReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest as FileDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest as TextDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest as WebDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.inners.models.value_objects.contracts.responses.passage_search.process_response import ProcessResponse
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement
from app.inners.use_cases.passage_search.ranker_model import RankerModel
from app.inners.use_cases.passage_search.retriever_model import RetrieverModel
from app.inners.use_cases.utilities.document_processor import DocumentProcessor
from app.inners.use_cases.utilities.locker import Locker
from app.outers.settings.datastore_one_setting import DatastoreOneSetting
from app.outers.settings.datastore_two_setting import DatastoreTwoSetting


class PassageSearch:

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.retriever_model = RetrieverModel()
        self.ranker_model = RankerModel()
        self.datastore_one_setting = DatastoreOneSetting()
        self.datastore_two_setting = DatastoreTwoSetting()
        self.document_management = DocumentManagement()
        self.document_type_management = DocumentTypeManagement()
        self.file_document_management = FileDocumentManagement()
        self.text_document_management = TextDocumentManagement()
        self.web_document_management = WebDocumentManagement()

    async def get_corpus(self, document: Document, document_type: DocumentType) -> str:
        if document_type.name == "file":
            found_detail_document: Content[FileDocumentResponse] = await self.file_document_management.read_one_by_id(
                request=FileDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            file_name: str = found_detail_document.data.file_name
            file_extension: str = found_detail_document.data.file_extension
            file_path: Path = Path(f"app/outers/persistences/temps/{file_name}{file_extension}")
            file_bytes: bytes = found_detail_document.data.file_bytes
            with open(file_path, "wb") as file:
                file.write(file_bytes)
            corpus = file_path
        elif document_type.name == "text":
            found_detail_document: Content[TextDocumentResponse] = await self.text_document_management.read_one_by_id(
                request=TextDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.text_content
        elif document_type.name == "web":
            found_detail_document: Content[WebDocumentResponse] = await self.web_document_management.read_one_by_id(
                request=WebDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.web_url
        else:
            raise Exception(f"Document type id {document_type.id} not yet supported.")

        return corpus

    async def get_window_sized_documents(self, process_body: ProcessBody) -> List[Document]:
        found_document: Content[Document] = await self.document_management.read_one_by_id(
            request=DocumentReadOneByIdRequest(
                id=process_body.input_setting.document_id
            )
        )

        found_document_type: Content[DocumentType] = await self.document_type_management.read_one_by_id(
            request=DocumentTypeReadOneByIdRequest(
                id=found_document.data.document_type_id
            )
        )

        window_sized_documents: List[DocumentHaystack] = self.document_processor.process(
            corpus=await self.get_corpus(
                document=found_document.data,
                document_type=found_document_type.data
            ),
            corpus_source_type=found_document_type.data.name,
            granularity=process_body.input_setting.granularity,
            window_sizes=process_body.input_setting.window_sizes
        )

        return window_sized_documents

    def get_document_store_index_hash(self, input_setting: InputSettingBody) -> str:
        hash_source: dict = {
            "document_id": input_setting.document_id,
            "granularity": input_setting.granularity,
            "window_sizes": input_setting.window_sizes,
            "embedding_model": input_setting.dense_retriever.embedding_model,
            "similarity_function": input_setting.dense_retriever.similarity_function
        }
        return hashlib.md5(str(hash_source).encode("utf-8")).hexdigest()

    @Locker.wait_lock
    def get_dense_retriever(self, process_body: ProcessBody, documents: List[DocumentHaystack]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            input_setting=process_body.input_setting
        )

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            port=self.datastore_two_setting.DS_2_PORT_1,
            index=f"dense_{document_store_index_hash}",
            embedding_dim=process_body.input_setting.dense_retriever.embedding_model.dimension,
            similarity=process_body.input_setting.dense_retriever.similarity_function,
        )

        retriever: BaseRetriever = self.retriever_model.get_dense_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.dense_retriever,
        )

        document_store.write_documents(documents)
        if process_body.input_setting.dense_retriever.is_update is True:
            document_store.update_embeddings(retriever)

        return retriever

    def get_sparse_retriever(self, process_body: ProcessBody, documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            input_setting=process_body.input_setting
        )

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            port=self.datastore_two_setting.DS_2_PORT_1,
            index=f"sparse_{document_store_index_hash}",
            similarity=process_body.input_setting.sparse_retriever.similarity_function,
        )
        retriever: BaseRetriever = self.retriever_model.get_sparse_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.sparse_retriever,
        )
        document_store.write_documents(documents)

        return retriever

    def get_ranker(self, process_body: ProcessBody) -> BaseRanker:
        return self.ranker_model.get_ranker(
            ranker_body=process_body.input_setting.ranker
        )

    def get_pipeline(self, process_body: ProcessBody, documents: List[Document]) -> Pipeline:
        dense_retriever: BaseRetriever = self.get_dense_retriever(
            process_body=process_body,
            documents=documents
        )
        sparse_retriever: BaseRetriever = self.get_sparse_retriever(
            process_body=process_body,
            documents=documents
        )
        document_joiner: JoinDocuments = JoinDocuments(
            join_mode="reciprocal_rank_fusion"
        )
        ranker: BaseRanker = self.get_ranker(
            process_body=process_body
        )

        pipeline: Pipeline = Pipeline()
        pipeline.add_node(
            component=dense_retriever,
            name="DenseRetriever",
            inputs=["Query"]
        )
        pipeline.add_node(
            component=sparse_retriever,
            name="SparseRetriever",
            inputs=["Query"]
        )
        pipeline.add_node(
            component=document_joiner,
            name="DocumentJoiner",
            inputs=["DenseRetriever", "SparseRetriever"]
        )
        pipeline.add_node(
            component=ranker,
            name="Ranker",
            inputs=["DocumentJoiner"]
        )

        return pipeline

    async def search(self, process_request: ProcessRequest) -> Content[ProcessResponse]:
        time_start: datetime = datetime.now()

        window_sized_documents: List[DocumentHaystack] = await self.get_window_sized_documents(
            process_body=process_request.body
        )

        pipeline: Pipeline = self.get_pipeline(
            process_body=process_request.body,
            documents=window_sized_documents
        )

        retrieval_result: dict = pipeline.run(
            query=process_request.body.input_setting.query,
            params={
                "DenseRetriever": {"top_k": process_request.body.input_setting.dense_retriever.top_k},
                "SparseRetriever": {"top_k": process_request.body.input_setting.sparse_retriever.top_k},
                "Ranker": {"top_k": process_request.body.input_setting.ranker.top_k}
            },
            debug=True
        )

        time_finish: datetime = datetime.now()
        time_delta: timedelta = time_finish - time_start

        response: ProcessResponse = ProcessResponse(
            retrieval_result=retrieval_result,
            process_duration=time_delta.total_seconds()
        )

        content: Content = Content(
            message="Passage search succeed.",
            data=response,
        )

        return content
