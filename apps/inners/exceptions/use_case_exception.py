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


class ExistingGeneratedHallucinationGradeHashInvalid(BaseException):
    pass


class EmbeddingFunctionalityNotSupported(BaseException):
    pass


class QueryInstructionNotProvided(BaseException):
    pass


class ExistingGeneratedAnswerRelevancyGradeHashInvalid(BaseException):
    pass


class ExistingGeneratedQuestionHashInvalid(BaseException):
    pass


class LlmProviderNotSupported(BaseException):
    pass


class ExistingRelevantDocumentHashInvalid(BaseException):
    pass


class RerankError(BaseException):
    pass


class RerankerModelNameNotSupported(BaseException):
    pass


class ExistingReRankedDocumentHashInvalid(BaseException):
    pass
