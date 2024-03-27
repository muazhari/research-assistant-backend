from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.interfaces.deliveries.middlewares.authorization_middleware import AuthorizationMiddleware
from apps.outers.interfaces.deliveries.middlewares.session_middleware import SessionMiddleware


class MiddlewareContainer(DeclarativeContainer):
    datastores = providers.DependenciesContainer()

    session = providers.Singleton(
        SessionMiddleware,
        one_datastore=datastores.one_datastore,
    )
    authorization = providers.Singleton(
        AuthorizationMiddleware
    )
