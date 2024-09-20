import inspect
from typing import List, Optional

from apps.inners.models.base_model import BaseModel


class Caller(BaseModel):
    file_name: Optional[str]
    class_name: Optional[str]
    function_name: Optional[str]


def get_callers_from_traces(traces) -> List[Caller]:
    callers: List[Caller] = []
    for trace in traces:
        f_locals = trace.frame.f_locals.get("self", None)
        if f_locals is None:
            class_name = None
        else:
            class_name = f_locals.__class__.__name__

        caller: Caller = Caller(
            file_name=trace.filename,
            class_name=class_name,
            function_name=trace.function
        )
        callers.append(caller)

    return callers


def get_last_caller() -> Caller:
    callers: List[Caller] = get_callers_from_traces(
        traces=inspect.trace()
    )
    last_caller: Caller = callers[-1]
    return last_caller
