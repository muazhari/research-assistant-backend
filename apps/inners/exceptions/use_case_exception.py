from apps.inners.exceptions.base_exception import BaseException


class PasswordNotMatched(BaseException):
    pass


class EmailAlreadyExists(BaseException):
    pass


class DocumentTypeNotSupported(BaseException):
    pass


class EmbeddingModelNameNotSupported(BaseException):
    pass


class ExistingCategorizedDocumentHashInvalid(BaseException):
    pass


class DocumentStoreRetrieveError(BaseException):
    pass


class ExistingGeneratedAnswerHashInvalid(BaseException):
    pass
