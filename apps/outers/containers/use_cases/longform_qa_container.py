from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.inners.use_cases.long_form_qas.process_longform_qa import ProcessLongFormQa


class LongFormQAContainer(DeclarativeContainer):
    graphs = providers.DependenciesContainer()

    process = providers.Singleton(
        ProcessLongFormQa,
        long_form_qa_graph=graphs.long_form_qa,
    )
