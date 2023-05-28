import json

import pytest as pytest
import pytest_asyncio

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.file_document import FileDocument
from app.inners.models.entities.text_document import TextDocument
from app.inners.models.entities.web_document import WebDocument
from app.inners.models.value_objects.contracts.requests.embedding_model_body import EmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from test.app.outers.interfaces.deliveries.controllers.account_controller_test import account_repository
from test.app.outers.interfaces.deliveries.controllers.document_controller_test import document_repository
from test.app.outers.interfaces.deliveries.controllers.document_type_controller_test import document_type_repository
from test.app.outers.interfaces.deliveries.controllers.file_document_controller_test import file_document_repository
from test.app.outers.interfaces.deliveries.controllers.text_document_controller_test import text_document_repository
from test.app.outers.interfaces.deliveries.controllers.web_document_controller_test import web_document_repository
from test.mock_data.passage_search_mock_data import PassageSearchMockData
from test.utilities.test_client_utility import get_async_client

test_client = get_async_client()
passage_search_mock_data = PassageSearchMockData()
data = passage_search_mock_data.get_data()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def run_around(request: pytest.FixtureRequest):
    for account in data["account"]:
        await account_repository.create_one(Account(**account.dict()))
    for document_type in data["document_type"]:
        await document_type_repository.create_one(DocumentType(**document_type.dict()))
    for document in data["document"]:
        await document_repository.create_one(Document(**document.dict()))
    for file_document in data["file_document"]:
        await file_document_repository.create_one(FileDocument(**file_document.dict()))
    for text_document in data["text_document"]:
        await text_document_repository.create_one(TextDocument(**text_document.dict()))
    for web_document in data["web_document"]:
        await web_document_repository.create_one(WebDocument(**web_document.dict()))

    yield

    for file_document in data["file_document"]:
        await file_document_repository.delete_one_by_id(file_document.id)
    for text_document in data["text_document"]:
        await text_document_repository.delete_one_by_id(text_document.id)
    for web_document in data["web_document"]:
        await web_document_repository.delete_one_by_id(web_document.id)
    for document in data["document"]:
        await document_repository.delete_one_by_id(document.id)
    for document_type in data["document_type"]:
        await document_type_repository.delete_one_by_id(document_type.id)
    for account in data["account"]:
        await account_repository.delete_one_by_id(account.id)


@pytest.mark.asyncio
async def test__passage_search_in_text__should_process_it__success():
    # Arrange
    body = ProcessBody(
        corpus_source_type="text",
        corpus=data["text_document"][0].text_content,
        query="definition of software engineering",
        granularity="sentence",
        window_sizes=[1, 2, 3, 4, 5],
        retriever_source_type="local",
        dense_retriever="dense_passage",
        sparse_retriever="bm25",
        ranker="sentence_transformers",
        embedding_model=EmbeddingModelBody(
            query_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
            passage_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
            ranker_model="naver/trecdl22-crossencoder-electra"
        ),
        embedding_dimension=128,
        num_iterations=None,
        similarity_function="dot_product",
        retriever_top_k=100,
        ranker_top_k=15,
        api_key=None
    )
    response = await test_client.post(
        url="/api/v1/passage-search",
        json=json.loads(body.json())
    )

    print(response)
