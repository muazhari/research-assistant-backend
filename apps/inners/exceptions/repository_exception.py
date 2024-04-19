from apps.inners.exceptions.base_exception import BaseException


class NotFound(BaseException):
    pass


class IntegrityError(BaseException):
    pass
