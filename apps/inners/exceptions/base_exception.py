import inspect
from types import FrameType
from typing import Optional, Any

from tools.caller_tool import Caller


class BaseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        last_frame: Optional[FrameType] = inspect.currentframe().f_back
        f_locals: Optional[Any] = last_frame.f_locals.get("self", None)
        if f_locals is None:
            class_name = None
        else:
            class_name = f_locals.__class__.__name__
        self.caller: Caller = Caller(
            file_name=last_frame.f_code.co_filename,
            class_name=class_name,
            function_name=last_frame.f_code.co_name,
        )
