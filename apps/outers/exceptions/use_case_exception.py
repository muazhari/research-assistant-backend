from apps.outers.exceptions.base_exception import BaseException


class PasswordNotMatched(BaseException):
    pass


class EmailAlreadyExists(BaseException):
    pass
