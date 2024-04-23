from datetime import timezone, datetime
from typing import Dict, Any, List

import pytest as pytest
from httpx import Response
from starlette import status
from unstructured.partition.utils.constants import PartitionStrategy

from apps.inners.models.daos.document import Document
from apps.inners.models.daos.session import Session
from apps.inners.models.dtos.content import Content
from apps.inners.models.dtos.contracts.requests.long_form_qas.input_setting_body import InputSettingBody, \
    GeneratorSetting
from apps.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from apps.inners.models.dtos.contracts.requests.passage_searches.input_setting_body import LlmSetting, \
    PreprocessorSetting, EmbedderSetting, RetrieverSetting, RerankerSetting
from apps.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from tests.main_context import MainContext

url_path: str = "/api/long-form-qas"


@pytest.mark.asyncio
async def test__process__should_processed__succeed(main_context: MainContext):
    selected_session_fake: Session = main_context.all_seeder.session_seeder.session_fake.data[0]
    selected_document_fakes: List[Document] = [
        main_context.all_seeder.document_seeder.document_fake.data[1],
        main_context.all_seeder.document_seeder.document_fake.data[2]
    ]
    process_body: ProcessBody = ProcessBody(
        input_setting=InputSettingBody(
            document_ids=[selected_session_fake.id for selected_session_fake in selected_document_fakes],
            llm_setting=LlmSetting(
                model_name="claude-3-haiku-20240307",
                max_token=500
            ),
            preprocessor_setting=PreprocessorSetting(
                is_force_refresh_categorized_element=False,
                is_force_refresh_categorized_document=False,
                file_partition_strategy=PartitionStrategy.AUTO,
                chunk_size=500,
                overlap_size=50,
                is_include_table=False,
                is_include_image=False
            ),
            embedder_setting=EmbedderSetting(
                is_force_refresh_embedding=False,
                is_force_refresh_document=False,
                model_name="BAAI/bge-m3",
                query_instruction="Given the question, retrieve passage that answer the question."
            ),
            retriever_setting=RetrieverSetting(
                is_force_refresh_relevant_document=False,
                top_k=50
            ),
            reranker_setting=RerankerSetting(
                is_force_refresh_re_ranked_document=False,
                model_name="BAAI/bge-reranker-v2-m3",
                top_k=5
            ),
            question="what is political science?",
            generator_setting=GeneratorSetting(
                is_force_refresh_generated_answer=False,
                is_force_refresh_generated_question=False,
                is_force_refresh_generated_hallucination_grade=False,
                is_force_refresh_generated_answer_relevancy_grade=False,
                prompt="""Instruction: Create a concise and informative answer for a given question based solely on the given passages. You must only use information from the given passages. Use an academic style. Do not repeat text. Cite at least one passage in each sentence. Cite the passages using passage number notation like "[number]". If multiple passages contain the answer, cite those passages like "[number, number, etc.]". If the passages do not contain the answer to the question, then say that answering is not possible given the available information with the explanation. Ensure the output is not re-explaining the instruction.
                Passages:
                {% for passage in passages %}
                [{{ loop.index }}]={{ passage.page_content }}
                {% endfor %}
                Question: {{ question }}
                Answer:"""
            ),
            transform_question_max_retry=3
        )
    )
    headers: Dict[str, Any] = {
        "Authorization": f"Bearer {selected_session_fake.access_token}"
    }
    response: Response = await main_context.client.post(
        url=url_path,
        headers=headers,
        json=process_body.model_dump(mode="json")
    )

    content: Content[ProcessResponse] = Content[ProcessResponse](
        **response.json(),
        status_code=response.status_code
    )
    assert content.status_code == status.HTTP_200_OK
    assert len(content.data.re_ranked_documents) >= 1
    assert len(content.data.generated_answer) >= 1
    assert content.data.started_at <= datetime.now(tz=timezone.utc)
    assert content.data.finished_at <= datetime.now(tz=timezone.utc)
