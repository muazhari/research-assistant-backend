import hashlib
import threading
from functools import wraps

locks = {}


class Locker:
    @staticmethod
    def wait_lock(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name_hash = hashlib.md5(func.__name__.encode()).hexdigest()
            func_args_hash = hashlib.md5(str(args).encode()).hexdigest()
            func_kwargs_hash = hashlib.md5(str(kwargs).encode()).hexdigest()
            func_hash = f"{func_name_hash}_{func_args_hash}_{func_kwargs_hash}"
            locks[func_hash] = locks.get(func_hash, threading.Lock())
            with locks[func_hash]:
                result = func(*args, **kwargs)
            return result

        return wrapper
