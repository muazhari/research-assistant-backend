import base64


def java_encode(string_to_encode: str) -> list[int]:
    encoding_1 = string_to_encode.encode(encoding="utf-8")
    encoding_2 = convert_python_bytes_to_java_bytes(encoding_1)
    return encoding_2


def java_decode(string_to_decode: list[int]) -> str:
    decoding_1 = convert_java_bytes_to_python_bytes(string_to_decode)
    decoding_2 = decoding_1.decode(encoding="utf-8")
    return decoding_2


def b64_encode(string_to_encode: str) -> bytes:
    encoding_1 = string_to_encode.encode(encoding="utf-8")
    encoding_2 = base64.b64encode(encoding_1)
    return encoding_2


def b64_decode(string_to_decode: bytes) -> str:
    decoding_1 = base64.b64decode(string_to_decode)
    decoding_2 = decoding_1.decode(encoding="utf-8")
    return decoding_2


def convert_python_bytes_to_java_bytes(bytes_to_convert: bytes) -> list[int]:
    return [x % 256 for x in bytes_to_convert]


def convert_java_bytes_to_python_bytes(bytes_to_convert: list[int]) -> bytes:
    decoding_1 = [x % 256 for x in bytes_to_convert]
    decoding_2 = bytes(decoding_1)
    return decoding_2
