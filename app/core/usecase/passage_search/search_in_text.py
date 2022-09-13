import time

from app.core.usecase.crud import account_crud, document_crud, document_type_crud
from app.core.usecase.document_store.document_creator import create_text_document, create_file_document
from app.infrastucture.delivery.contract.request.document_search.document_search_request import DocumentSearchRequest
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import \
    BaseDocumentSearchResponse
from app.infrastucture.delivery.contract.response.document_search.file_document_search_response import \
    FileDocumentSearchResponse
from app.infrastucture.delivery.contract.response.document_search.text_document_search_response import \
    TextDocumentSearchResponse


# from haystack.pipeline import Pipeline

def search_passage_in_text(search_request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    found_account = account_crud.find_one_by_id(search_request.account_id)
    found_document = document_crud.find_one_by_id(search_request.document_id)
    found_conversion_document_type = document_type_crud.find_one_by_id(
        search_request.conversion_document_type_id)

    time_start = time.time()

    # pipeline = Pipeline()
    # pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    # pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
    # pipeline.add_node(component=retriever, name="EmbeddingRetriever", inputs=["PreProcessor"])
    # pipeline.add_node(component=document_store, name="DeepsetCloudDocumentStore", inputs="EmbeddingRetriever")

    time_finish = time.time()
    process_duration = time_finish - time_start

    response = None
    if found_conversion_document_type.name == 'text':
        response = convert_to_text(search_request, process_duration)
    elif found_conversion_document_type.name == 'file':
        response = convert_to_file(search_request, process_duration)
    return response


def convert_to_text(search_request, process_duration):
    processed_document = create_text_document(
        name="processed document",
        description="processed description",
        account_id=search_request.account_id,
        text_content="processed text content"
    )

    response = TextDocumentSearchResponse(
        processed_document=processed_document["document"],
        processed_text_document=processed_document["text_document"],
        process_duration=process_duration
    )

    return response


def convert_to_file(search_request, process_duration):
    time_start = time.time()

    processed_document = create_file_document(
        name="processed document",
        description="processed description",
        account_id=search_request.account_id,
        file_name="processed file name",
        file_extension="pfe",
        file_bytes=b"processed file byte"
    )
    time_finish = time.time()
    process_duration = time_finish - time_start
    response = FileDocumentSearchResponse(
        processed_document=processed_document["document"],
        processed_file_document=processed_document["file_document"],
        process_duration=process_duration
    )

    return response
