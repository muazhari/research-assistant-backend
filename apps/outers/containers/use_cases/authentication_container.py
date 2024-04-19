from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.authentications.login_authentication import LoginAuthentication
from apps.inners.use_cases.authentications.logout_authentication import LogoutAuthentication
from apps.inners.use_cases.authentications.register_authentication import RegisterAuthentication


class AuthenticationContainer(DeclarativeContainer):
    managements = providers.DependenciesContainer()

    login = providers.Singleton(
        LoginAuthentication,
        account_management=managements.account,
        session_management=managements.session,
    )
    register = providers.Singleton(
        RegisterAuthentication,
        account_management=managements.account,
    )
    logout = providers.Singleton(
        LogoutAuthentication,
        session_management=managements.session,
    )
