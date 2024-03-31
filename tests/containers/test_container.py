from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.containers.application_container import ApplicationContainer
from tests.containers.mock_container import MockContainer
from tests.containers.seeder_container import SeederContainer
from tests.main_context import MainContext


class TestContainer(DeclarativeContainer):
    applications = providers.Container(
        ApplicationContainer
    )
    mocks = providers.Container(
        MockContainer
    )
    seeders = providers.Container(
        SeederContainer,
        datastores=applications.datastores,
        mocks=mocks,
    )
    main_context = providers.Singleton(
        MainContext,
        all_seeder=seeders.all
    )
