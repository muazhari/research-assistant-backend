from typing import Dict, Any, Union, List


def replace_end_value_to_string(d: Dict[Any, Any]) -> Dict[Any, Any]:
    replaced_dict: Dict[Any, Any] = {}
    for key in d.keys():
        value: Any = d[key]
        if isinstance(value, Dict):
            replaced_dict[key] = replace_end_value_to_string(value)
        elif isinstance(value, List):
            replaced_dict[key] = list(map(replace_end_value_to_string, value))
        else:
            replaced_dict[key] = str(value)

    return replaced_dict


def filter_by_keys(d: Dict[Any, Any], keys: Union[List[Any] | Any]) -> Dict[Any, Any]:
    if not isinstance(d, Dict):
        return d

    filtered_dict: Dict[Any, Any] = {}
    if isinstance(keys, Dict):
        keys_keys: List[Any] = list(keys.keys())
        for d_key in d.keys():
            d_value: Any = d[d_key]
            if d_key in keys_keys:
                filtered_dict[d_key] = filter_by_keys(d_value, keys[d_key])
    elif isinstance(keys, List):
        for d_key in d.keys():
            d_value: Any = d[d_key]
            for key in keys:
                if isinstance(key, Dict):
                    key_keys: List[Any] = list(key.keys())
                    if d_key in key_keys:
                        filtered_dict[d_key] = filter_by_keys(d_value, key[d_key])
                else:
                    if d_key == key:
                        filtered_dict[d_key] = d_value
    else:
        filtered_dict = d

    return filtered_dict
