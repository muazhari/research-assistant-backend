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
from apps.inners.models.dtos.contracts.result import Result
from apps.inners.use_cases.authorizations.session_authorization import SessionAuthorization
from apps.outers.containers.application_container import ApplicationContainer

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
        type_param: str = request.query_params.get("type")
        if type_param is None:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[Session](
                    message=f"AuthorizationController.refresh: refresh {type_param} is required.",
                    data=None
                ).json()
            )
            return response

        if type_param == "access_token":
            result: Result[Session] = await self.session_authorization.refresh_access_token(
                state=request.state,
                body=body
            )
            response: Response = Response(
                status_code=result.status_code,
                content=Content[Session](
                    message="AuthorizationController.refresh: refresh access token success.",
                    data=result.data
                ).json()
            )
        else:
            response: Response = Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=Content[Session](
                    message=f"AuthorizationController.refresh: refresh {type_param} is not supported.",
                    data=None
                ).json()
            )

        return response
