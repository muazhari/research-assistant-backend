from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from app.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware


class MiddlewareContainer(DeclarativeContainer):
    datastores = providers.DependenciesContainer()

    session_middleware = providers.Singleton(
        SessionMiddleware,
        one_datastore=datastores.one_datastore,
    )

    authorization_middleware = providers.Singleton(
        AuthorizationMiddleware,
        one_datastore=datastores.one_datastore,
    )
