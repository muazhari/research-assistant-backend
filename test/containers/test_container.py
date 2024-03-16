from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.outers.containers.application_container import ApplicationContainer
from test.containers.mock_container import MockContainer
from test.containers.seeder_container import SeederContainer


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
