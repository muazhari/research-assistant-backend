from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.inners.use_cases.long_form_qa.longform_qa import LongFormQA


class LongFormQAContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    utilities = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()

    longform_qa = providers.Singleton(
        LongFormQA,
    )