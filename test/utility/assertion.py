import json


def assert_dict_keys_equal(expected: dict, actual: dict) -> bool:
    return expected.keys() == actual.keys()


def assert_dict_values_type_equal(expected: dict, actual: dict) -> bool:
    return list(map(type, expected.values())) == list(map(type, expected.values()))


def assert_json_keys_equal(expected: str, actual: str) -> bool:
    expected_json = json.loads(expected)
    actual_json = json.loads(actual)
    return assert_dict_keys_equal(expected_json, actual_json)


def assert_json_values_type_equal(expected: str, actual: str) -> bool:
    expected_json = json.loads(expected)
    actual_json = json.loads(actual)
    return assert_dict_values_type_equal(expected_json, actual_json)


def assert_json_structure_equal(expected: str, actual: str) -> bool:
    expected_json = json.loads(expected)
    actual_json = json.loads(actual)
    is_json_keys_equal: bool = assert_json_keys_equal(expected_json, actual_json)
    is_json_values_type_equal: bool = assert_json_values_type_equal(expected_json, actual_json)
    return is_json_values_type_equal and is_json_keys_equal


def assert_dict_structure_equal(expected: dict, actual: dict) -> bool:
    is_dict_keys_equal: bool = assert_dict_keys_equal(expected, actual)
    is_dict_values_type_equal: bool = assert_dict_values_type_equal(expected, actual)
    return is_dict_values_type_equal and is_dict_keys_equal
