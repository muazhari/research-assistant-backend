import json

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.file_document import FileDocument
from app.inners.models.entities.text_document import TextDocument
from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.basic_settings.dense_embedding_model_body import \
    DenseEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.basic_settings.dense_retriever_body import DenseRetrieverBody
from app.inners.models.value_objects.contracts.requests.basic_settings.document_setting_body import DocumentSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.sentence_transformers_ranker_body import \
    SentenceTransformersRankerModelBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.output_setting_body import OutputSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.ranker_body import RankerBody
from app.inners.models.value_objects.contracts.requests.basic_settings.sparse_retriever_body import SparseRetrieverBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.passage_searchs.process_response import ProcessResponse
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.app.outers.interfaces.deliveries.controllers.file_document_controller_test import file_document_repository
from test.app.outers.interfaces.deliveries.controllers.text_document_controller_test import text_document_repository
from test.app.outers.interfaces.deliveries.controllers.web_document_controller_test import web_document_repository
from test.mock_data.passage_search_mock_data import PassageSearchMockData
from test.utilities.test_client_utility import get_async_client

passage_search_mock_data = PassageSearchMockData()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in passage_search_mock_data.account_data:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in passage_search_mock_data.document_type_data:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in passage_search_mock_data.document_data:
        await document_repository.create_one(Document(**document.dict()))
    for file_document in passage_search_mock_data.file_document_data:
        await file_document_repository.create_one(FileDocument(**file_document.dict()))
    for text_document in passage_search_mock_data.text_document_data:
        await text_document_repository.create_one(TextDocument(**text_document.dict()))
    for web_document in passage_search_mock_data.web_document_data:
        await web_document_repository.create_one(WebDocument(**web_document.dict()))

    yield

    for file_document in passage_search_mock_data.file_document_data:
        await file_document_repository.delete_one_by_id(file_document.id)
    for text_document in passage_search_mock_data.text_document_data:
        await text_document_repository.delete_one_by_id(text_document.id)
    for web_document in passage_search_mock_data.web_document_data:
        await web_document_repository.delete_one_by_id(web_document.id)
    for document in passage_search_mock_data.document_data:
        await document_repository.delete_one_by_id(document.id)
    for document_type in passage_search_mock_data.document_type_data:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in passage_search_mock_data.account_data:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__passage_search_in_text__should_process_it__success():
    body: ProcessBody = ProcessBody(
        account_id=passage_search_mock_data.account_data[0].id,
        input_setting=InputSettingBody(
            document_setting=DocumentSettingBody(
                document_id=passage_search_mock_data.document_data[1].id,
            ),
            query="definition of software engineering",
            granularity="sentence",
            window_sizes=[1, 2, 3],
            dense_retriever=DenseRetrieverBody(
                source_type="dense_passage",
                similarity_function="dot_product",
                is_update=True,
                top_k=100,
                embedding_model=DenseEmbeddingModelBody(
                    dimension=128,
                    query_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
                    passage_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
                ),
            ),
            sparse_retriever=SparseRetrieverBody(
                source_type="bm25",
                similarity_function="dot_product",
                top_k=100,
            ),
            ranker=RankerBody(
                source_type="sentence_transformers",
                ranker_model=SentenceTransformersRankerModelBody(
                    model="naver/trecdl22-crossencoder-electra"
                ),
                top_k=15,
            )
        ),
        output_setting=OutputSettingBody(
            document_type_id=passage_search_mock_data.document_type_data[1].id,
        )
    )

    async with get_async_client() as client:
        response = await client.post(
            url="/api/v1/passage-search",
            json=json.loads(body.json())
        )

        assert response.status_code == 200
        content: Content[ProcessResponse] = Content[ProcessResponse](**response.json())
        assert content.data is not None
