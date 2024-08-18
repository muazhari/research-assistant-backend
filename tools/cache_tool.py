import hashlib
import inspect
import json
from threading import Timer
from typing import Dict, Any, Union, List, Optional, Callable

from fastapi.encoders import jsonable_encoder

from tools import dict_tool

cache: Dict[Any, Any] = {}


def delete_cache(key: Any = None):
    if key is None:
        cache.clear()

    cache.pop(key, None)


def is_key_in_cache(key: Any) -> bool:
    return key in cache.keys()


def hash_by_dict(data: Dict[Any, Any]) -> str:
    string_data: bytes = json.dumps(
        obj=data,
        sort_keys=True,
        default=jsonable_encoder
    ).encode()
    hashed_data: str = hashlib.sha256(
        string=string_data
    ).hexdigest()

    return hashed_data


def get_cache(key: Optional[Any] = None, default_func: Optional[Callable] = None) -> Any:
    if key is None:
        return cache

    value: Any = cache.get(key, None)

    if value is None and default_func is not None:
        value = default_func()
        set_cache(key, value)

    return value


def set_cache(key: Any, value: Any, timeout: Optional[float] = None):
    cache[key] = value

    if timeout is not None:
        timer: Timer = Timer(timeout, delete_cache, args=[key])
        timer.start()

