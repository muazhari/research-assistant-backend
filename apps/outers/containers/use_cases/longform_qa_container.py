from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.long_form_qas.process_longform_qa import ProcessLongFormQA


class LongFormQAContainer(DeclarativeContainer):
    settings = providers.DependenciesContainer()
    datastores = providers.DependenciesContainer()
    utilities = providers.DependenciesContainer()
    managements = providers.DependenciesContainer()

    process = providers.Singleton(
        ProcessLongFormQA,
    )
