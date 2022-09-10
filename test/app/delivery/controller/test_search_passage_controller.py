import json

from app.core.model.entity.text_document import TextDocument
from test.utility.assertion import assert_dict_structure_equal


def test_search_passage_text_on_success():
    # document_text_mock = TextDocument(**json.load(open("test/mock_data/document_text.json")))
    request_dict_mock = json.load(open("test/mock_data/search_passage_request.json"))
    response_dict_mock = json.load(open("test/mock_data/search_passage_response.json"))

    response = client.post(url="api/v1/search/passage/text", json=request_dict_mock)

    assert response.status_code == 200
    assert assert_dict_structure_equal(response.json(), response_dict_mock)


def test_search_passage_text_on_failure():
    request_data = json.load(open("test/mock_data/search_passage_request.json"))
    response_data = json.load(open("test/mock_data/search_passage_response.json"))
    response = client.post("api/v1/document_search/text", json=None)

    assert response.status_code == 422
