from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest
from apps.inners.models.dtos.contracts.requests.passage_searches.input_setting_body import \
    InputSettingBody as InputSettingBodyPassageSearch


class GeneratorSetting(BaseRequest):
    is_force_refresh_generated_answer: bool
    is_force_refresh_generated_question: bool
    is_force_refresh_generated_hallucination_grade: bool
    is_force_refresh_generated_answer_relevancy_grade: bool
    prompt: str


class InputSettingBody(InputSettingBodyPassageSearch):
    generator_setting: GeneratorSetting
    transform_question_max_retry: int
