import hashlib
import threading
from functools import wraps


class Locker:
    locks = {}

    @staticmethod
    def wait_lock(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name_hash = hashlib.md5(func.__name__.encode()).hexdigest()
            func_args_hash = hashlib.md5(str(args).encode()).hexdigest()
            func_kwargs_hash = hashlib.md5(str(kwargs).encode()).hexdigest()
            func_hash = f"{func_name_hash}_{func_args_hash}_{func_kwargs_hash}"
            Locker.locks[func_hash] = Locker.locks.get(func_hash, threading.Lock())
            with Locker.locks[func_hash]:
                result = func(*args, **kwargs)
            return result

        return wrapper
