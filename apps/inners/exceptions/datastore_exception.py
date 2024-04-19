from apps.inners.exceptions.base_exception import BaseException


class MaxRetriesExceeded(BaseException):
    pass


class HandlerError(BaseException):
    pass
