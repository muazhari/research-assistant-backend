from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.authorizations.session_authorization import SessionAuthorization


class AuthorizationContainer(DeclarativeContainer):
    managements = providers.DependenciesContainer()

    session = providers.Singleton(
        SessionAuthorization,
        session_management=managements.session,
        account_management=managements.account
    )
