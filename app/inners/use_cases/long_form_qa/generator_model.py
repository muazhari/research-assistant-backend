from haystack.nodes import PromptNode, PromptTemplate, AnswerParser

from app.inners.models.value_objects.contracts.requests.basic_settings.generator_body import GeneratorBody
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody


class GeneratorModel:
    def get_online_generator(self, generator_body: GeneratorBody) -> PromptNode:
        prompt_template = PromptTemplate(
            prompt=generator_body.prompt,
            output_parser=AnswerParser()
        )

        generator: PromptNode = PromptNode(
            model_name_or_path=generator_body.generator_model.model,
            default_prompt_template=prompt_template,
            max_length=generator_body.answer_max_length,
            api_key=generator_body.generator_model.api_key,
            use_gpu=True,
        )
        return generator

    def get_generator(self, process_body: ProcessBody) -> PromptNode:
        if process_body.input_setting.generator.source_type == "online":
            generator: PromptNode = self.get_online_generator(
                generator_body=process_body.input_setting.generator,
            )
        else:
            raise ValueError(
                f"Generator source type {process_body.input_setting.generator.source_type} is not supported."
            )
        return generator
