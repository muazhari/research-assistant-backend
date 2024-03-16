from typing import Optional, List, Type

from fastapi.routing import APIRoute
from starlette.middleware import Middleware


def MiddlewareWrapper(middleware: Optional[List[Middleware]] = None) -> Type[APIRoute]:
    class CustomAPIRoute(APIRoute):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            app = self.app
            for cls, options in reversed(middleware or []):
                app = cls(app, **options)
            self.app = app

    return CustomAPIRoute
