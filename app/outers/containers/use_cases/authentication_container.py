from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.authentications.login_authentication import LoginAuthentication
from app.inners.use_cases.authentications.register_authentication import RegisterAuthentication
from app.outers.containers.use_cases.management_container import ManagementContainer


class AuthenticationContainer(DeclarativeContainer):
    managements: ManagementContainer = providers.DependenciesContainer()

    login: LoginAuthentication = providers.Singleton(
        LoginAuthentication,
        account_management=managements.account,
    )
    register: RegisterAuthentication = providers.Singleton(
        RegisterAuthentication,
        account_management=managements.account,
    )
