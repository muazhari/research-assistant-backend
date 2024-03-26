from datetime import datetime

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class CreateOneBody(BaseRequest):
    access_token: str
    refresh_token: str
    access_token_expired_at: datetime
    refresh_token_expired_at: datetime
