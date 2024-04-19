from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.exceptions import repository_exception, use_case_exception
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse
from apps.inners.use_cases.passage_searches.process_passage_search import ProcessPassageSearch


class PassageSearchController:

    def __init__(
            self,
            process_passage_search: ProcessPassageSearch
    ):
        self.router: APIRouter = APIRouter(
            tags=["passage-searches"],
            prefix="/passage-searches"
        )
        self.router.add_api_route(
            path="",
            endpoint=self.process,
            methods=["POST"]
        )
        self.process_passage_search = process_passage_search

    async def process(self, request: Request, body: ProcessBody) -> Response:
        content: Content[ProcessResponse] = Content[ProcessResponse](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.process.__name__}: Failed.",
            data=None
        )
        try:
            data: ProcessResponse = await self.process_passage_search.process(
                state=request.state,
                body=body
            )
            content.status_code = status.HTTP_200_OK
            content.data = data
        except repository_exception.IntegrityError as exception:
            content.status_code = status.HTTP_409_CONFLICT
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except repository_exception.NotFound as exception:
            content.status_code = status.HTTP_404_NOT_FOUND
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.DocumentTypeNotSupported as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.EmbeddingModelNameNotSupported as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.ExistingCategorizedDocumentHashInvalid as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.DocumentStoreRetrieveError as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.EmbeddingFunctionalityNotSupported as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.QueryInstructionNotProvided as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.LlmProviderNotSupported as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.ExistingRelevantDocumentHashInvalid as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.RerankError as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.RerankerModelNameNotSupported as exception:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."
        except use_case_exception.ExistingReRankedDocumentHashInvalid as exception:
            content.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            content.message += f" {exception.caller.class_name}.{exception.caller.function_name}: {exception.__class__.__name__}."

        return content.to_response()
