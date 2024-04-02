import hashlib
import inspect
import json
from typing import Dict, Any, Union, List

from fastapi.encoders import jsonable_encoder

from tools import dict_tool

cache: Dict[Any, Any] = {}


def clear_cache(keys: List[Any] = None):
    global cache
    if keys is None:
        cache = {}
    else:
        for key in keys:
            cache.pop(key, None)


def get_cache():
    return cache


def cacher(args_include_keys: Union[List[Any] | Any] = None, kwargs_include_keys: Union[List[Any] | Any] = None):
    def decorator(func):

        def wrapper(*args, **kwargs):
            dict_args: Dict[Any, Any] = {}
            if args_include_keys is None:
                _args_include_keys: Union[List[Any] | Any] = []
                for key, arg in enumerate(args):
                    dict_args[key] = arg
                    _args_include_keys.append(key)
            else:
                _args_include_keys: Union[List[Any] | Any] = args_include_keys
                for key, arg in enumerate(args):
                    dict_args[key] = arg
            if kwargs_include_keys is None:
                _kwargs_include_keys: Union[List[Any] | Any] = kwargs.keys()
            else:
                _kwargs_include_keys: Union[List[Any] | Any] = kwargs_include_keys

            try:
                is_method = inspect.getfullargspec(func)[0][0] == 'self'
            except IndexError:
                is_method = False

            key_dict: Dict[str, Any] = {
                "module_name": func.__module__,
                "class_name": None,
                "function_name": func.__name__,
                "args": dict_tool.replace_end_value_to_string(dict_tool.filter_by_keys(dict_args, _args_include_keys)),
                "kwargs": dict_tool.replace_end_value_to_string(dict_tool.filter_by_keys(kwargs, _kwargs_include_keys)),
            }
            if is_method:
                key_dict["class_name"] = args[0].__class__.__name__

            key_hash: str = hashlib.sha256(
                string=json.dumps(
                    obj=key_dict,
                    default=jsonable_encoder,
                    sort_keys=True,
                ).encode()
            ).hexdigest()
            result: Any = cache.get(key_hash, None)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache[key_hash] = result

            return result

        return wrapper

    return decorator
