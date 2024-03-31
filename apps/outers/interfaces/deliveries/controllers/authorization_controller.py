from typing import Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.contracts.content import Content
from apps.inners.models.dtos.contracts.requests.authorizations.refresh_access_token_body import RefreshAccessTokenBody
from apps.inners.use_cases.authorizations.session_authorization import SessionAuthorization
from apps.outers.containers.application_container import ApplicationContainer
from apps.outers.exceptions import repository_exception

router: APIRouter = APIRouter(tags=["authorizations"])


@cbv(router)
class AuthorizationController:

    @inject
    def __init__(
            self,
            session_authorization: SessionAuthorization = Depends(
                Provide[ApplicationContainer.use_cases.authorizations.session]
            ),
    ):
        self.session_authorization = session_authorization

    @router.post("/authorizations/refreshes")
    async def refresh(self, request: Request, body: Union[RefreshAccessTokenBody]) -> Response:
        content: Content[Session] = Content[Session](
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{self.__class__.__name__}.{self.refresh.__name__}: Failed.",
            data=None
        )
        type_param: str = request.query_params.get("type")
        if type_param is None:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.refresh.__name__}: Type is required."
        elif type_param == "access_token":
            try:
                data: Session = await self.session_authorization.refresh_access_token(
                    state=request.state,
                    body=body
                )
                content.status_code = status.HTTP_200_OK
                content.message = f"{self.__class__.__name__}.{self.refresh.__name__}: Succeed."
                content.data = data
            except repository_exception.NotFound as exception:
                content.status_code = status.HTTP_404_NOT_FOUND
                content.message += f" {exception.__class__.__name__}."
        else:
            content.status_code = status.HTTP_400_BAD_REQUEST
            content.message += f" {self.__class__.__name__}.{self.refresh.__name__}: Invalid type."

        return content.to_response()
