from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.outers.containers.application_container import ApplicationContainer
from tests.containers.fake_container import FakeContainer
from tests.containers.seeder_container import SeederContainer
from tests.main_context import MainContext


class TestContainer(DeclarativeContainer):
    applications = providers.Container(
        ApplicationContainer
    )
    fakes = providers.Container(
        FakeContainer
    )
    seeders = providers.Container(
        SeederContainer,
        datastores=applications.datastores,
        fakes=fakes,
    )
    main_context = providers.Singleton(
        MainContext,
        all_seeder=seeders.all
    )
