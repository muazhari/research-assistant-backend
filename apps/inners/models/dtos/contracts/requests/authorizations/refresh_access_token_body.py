from apps.inners.models.dtos.base_dto import BaseDto


class RefreshAccessTokenBody(BaseDto):
    refresh_token: str
