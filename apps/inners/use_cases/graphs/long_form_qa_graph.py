from typing import Dict, List, Any

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph, END
from pydantic.v1 import Field

from apps.inners.exceptions import use_case_exception
from apps.inners.models.base_model import BaseModel
from apps.inners.models.dtos.graph_state import LongFormQaGraphState
from apps.inners.use_cases.graphs.passage_search_graph import PassageSearchGraph
from apps.inners.use_cases.retrievers.hybrid_milvus_retriever import HybridMilvusRetriever
from tools import cache_tool


class LongFormQaGraph(PassageSearchGraph):
    def __init__(
            self,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.compiled_graph: CompiledGraph = self.compile()

    async def node_generate_answer(self, input_state: LongFormQaGraphState) -> LongFormQaGraphState:
        output_state: LongFormQaGraphState = input_state

        re_ranked_documents: List[Document] = input_state["re_ranked_documents"]
        retriever: HybridMilvusRetriever = input_state["retriever_setting"]["retriever"]
        re_ranked_document_ids: List[str] = [document.metadata[retriever.id_key] for document in re_ranked_documents]
        generated_answer_hash: str = self.get_generated_answer_hash(
            re_ranked_document_ids=re_ranked_document_ids,
            question=input_state["question"],
            llm_model_name=input_state["llm_setting"]["model_name"],
            prompt=input_state["generator_setting"]["prompt"],
            max_token=input_state["llm_setting"]["max_token"],
        )
        existing_generated_answer_hash: int = await self.two_datastore.async_client.exists(generated_answer_hash)
        if existing_generated_answer_hash == 0:
            is_generated_answer_exist: bool = False
        elif existing_generated_answer_hash == 1:
            is_generated_answer_exist: bool = True
        else:
            raise use_case_exception.ExistingGeneratedAnswerHashInvalid()

        is_force_refresh_generated_answer: bool = input_state["generator_setting"][
            "is_force_refresh_generated_answer"]
        if is_generated_answer_exist is False or is_force_refresh_generated_answer is True:
            prompt: PromptTemplate = PromptTemplate(
                template=input_state["generator_setting"]["prompt"],
                template_format="jinja2",
                input_variables=["passages", "question"]
            )
            text: str = prompt.format(
                passages=re_ranked_documents,
                question=input_state["question"]
            )
            messages: List[BaseMessage] = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                )
            ]
            llm_model: ChatLiteLLM = input_state["llm_setting"]["model"]
            chain: RunnableSerializable = llm_model | StrOutputParser()
            generated_answer: str = await chain.ainvoke(
                input=messages
            )
            await self.two_datastore.async_client.set(
                name=generated_answer_hash,
                value=generated_answer.encode()
            )
        else:
            generated_answer_byte: bytes = await self.two_datastore.async_client.get(generated_answer_hash)
            generated_answer: str = generated_answer_byte.decode()

        output_state["generated_answer"] = generated_answer
        output_state["generated_answer_hash"] = generated_answer_hash

        return output_state

    def get_generated_answer_hash(
            self,
            re_ranked_document_ids: List[str],
            question: str,
            llm_model_name: str,
            prompt: str,
            max_token: int,
    ) -> str:
        data: Dict[str, Any] = {
            "re_ranked_document_ids": re_ranked_document_ids,
            "question": question,
            "llm_model_name": llm_model_name,
            "prompt": prompt,
            "max_token": max_token,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"generated_answer/{hashed_data}"

        return hashed_data

    async def node_grade_hallucination(self, input_state: LongFormQaGraphState) -> LongFormQaGraphState:
        output_state: LongFormQaGraphState = input_state

        re_ranked_documents: List[Document] = input_state["re_ranked_documents"]

        class GradeTool(BaseModel):
            """Binary score for support check."""
            binary_score: bool = Field(
                description="Is supported binary score, either True if supported or False if not supported."
            )

        retriever: HybridMilvusRetriever = input_state["retriever_setting"]["retriever"]
        generated_hallucination_grade_hash: str = self.get_generated_hallucination_grade_hash(
            retrieved_document_ids=[document.metadata[retriever.id_key] for document in re_ranked_documents],
            generated_answer_hash=input_state["generated_answer_hash"]
        )
        existing_generated_hallucination_grade_hash: int = await self.two_datastore.async_client.exists(
            generated_hallucination_grade_hash)
        if existing_generated_hallucination_grade_hash == 0:
            is_generated_hallucination_grade_hash_exist: bool = False
        elif existing_generated_hallucination_grade_hash == 1:
            is_generated_hallucination_grade_hash_exist: bool = True
        else:
            raise use_case_exception.ExistingGeneratedHallucinationGradeHashInvalid()

        is_force_refresh_generated_hallucination_grade: bool = input_state["generator_setting"][
            "is_force_refresh_generated_hallucination_grade"]
        if is_generated_hallucination_grade_hash_exist is False or is_force_refresh_generated_hallucination_grade is True:
            prompt: PromptTemplate = PromptTemplate(
                template="""
                <instruction>
                Assess whether an Large Language Model generated answer to the question is supported by the passages. Give one binary score of "True" or "False". "True" means that the answer to the question is supported by the passages. "False" means that the answer to the question is not supported by the passages.
                <instruction/>
                <passages>
                {% for passage in passages %}
                <passage_{{ loop.index }}>
                {{ passage.page_content }}
                <passage_{{ loop.index }}/>
                {% endfor %}
                <passages/>
                <question>
                {{ question }}
                <question/>
                <answer>
                {{ answer }}
                <answer/>
                """,
                template_format="jinja2",
                input_variables=["passages", "question", "answer"]
            )
            text: str = prompt.format(
                passages=re_ranked_documents,
                question=input_state["question"],
                answer=input_state["generated_answer"]
            )
            messages: List[BaseMessage] = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                )
            ]
            llm_model: ChatLiteLLM = input_state["llm_setting"]["model"]
            tool_parser: PydanticToolsParser = PydanticToolsParser(
                tools=[GradeTool]
            )
            chain: RunnableSerializable = llm_model.bind_tools(tools=tool_parser.tools,
                                                               tool_choice="required") | tool_parser
            generated_tools: List[GradeTool] = await chain.ainvoke(
                input=messages
            )
            generated_hallucination_grade: str = str(not generated_tools[0].binary_score)
            await self.two_datastore.async_client.set(
                name=generated_hallucination_grade_hash,
                value=generated_hallucination_grade.encode()
            )
        else:
            generated_hallucination_grade_byte: bytes = await self.two_datastore.async_client.get(
                generated_hallucination_grade_hash)
            generated_hallucination_grade: str = generated_hallucination_grade_byte.decode()

        output_state["generated_hallucination_grade"] = generated_hallucination_grade
        output_state["generated_hallucination_grade_hash"] = generated_hallucination_grade_hash

        return output_state

    def get_generated_hallucination_grade_hash(
            self,
            retrieved_document_ids: List[str],
            generated_answer_hash: str,
    ) -> str:
        data: Dict[str, Any] = {
            "retrieved_document_ids": retrieved_document_ids,
            "generated_answer_hash": generated_answer_hash,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"generated_hallucination_grade/{hashed_data}"

        return hashed_data

    async def node_grade_answer_relevancy(self, input_state: LongFormQaGraphState) -> LongFormQaGraphState:
        output_state: LongFormQaGraphState = input_state

        class GradeTool(BaseModel):
            """Binary score for resolution check."""
            binary_score: bool = Field(
                description="Is resolved binary score, either True if resolved or False if not resolved."
            )

        generated_answer_relevancy_grade_hash: str = self.get_generated_answer_relevancy_grade_hash(
            question=input_state["question"],
            generated_answer_hash=input_state["generated_answer_hash"]
        )
        existing_generated_hallucination_grade_hash: int = await self.two_datastore.async_client.exists(
            generated_answer_relevancy_grade_hash)
        if existing_generated_hallucination_grade_hash == 0:
            is_generated_hallucination_grade_hash_exist: bool = False
        elif existing_generated_hallucination_grade_hash == 1:
            is_generated_hallucination_grade_hash_exist: bool = True
        else:
            raise use_case_exception.ExistingGeneratedAnswerRelevancyGradeHashInvalid()

        is_force_refresh_generated_answer_relevancy_grade: bool = input_state["generator_setting"][
            "is_force_refresh_generated_answer_relevancy_grade"]
        if is_generated_hallucination_grade_hash_exist is False or is_force_refresh_generated_answer_relevancy_grade is True:
            prompt: PromptTemplate = PromptTemplate(
                template="""
                <instruction>
                Assess whether an Large Language Model generated answer resolves a question. Give one binary score of "True" or "False". "True" means that the answer resolves the question. "False" means that the answer does not resolve the question.
                <instruction/>
                <question>
                {{ question }}
                <question/>
                <answer>
                {{ answer }}
                <answer/>
                """,
                template_format="jinja2",
                input_variables=["question", "answer"]
            )
            text: str = prompt.format(
                question=input_state["question"],
                answer=input_state["generated_answer"],
            )
            messages: List[BaseMessage] = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                )
            ]
            llm_model: ChatLiteLLM = input_state["llm_setting"]["model"]
            tool_parser: PydanticToolsParser = PydanticToolsParser(
                tools=[GradeTool]
            )
            chain: RunnableSerializable = llm_model.bind_tools(tools=tool_parser.tools,
                                                               tool_choice="required") | tool_parser
            generated_tools: List[GradeTool] = await chain.ainvoke(
                input=messages
            )
            generated_answer_relevancy_grade: str = str(generated_tools[0].binary_score)
            await self.two_datastore.async_client.set(
                name=generated_answer_relevancy_grade_hash,
                value=generated_answer_relevancy_grade.encode()
            )
        else:
            generated_answer_relevancy_grade_byte: bytes = await self.two_datastore.async_client.get(
                generated_answer_relevancy_grade_hash
            )
            generated_answer_relevancy_grade: str = generated_answer_relevancy_grade_byte.decode()

        output_state["generated_answer_relevancy_grade"] = generated_answer_relevancy_grade
        output_state["generated_answer_relevancy_grade_hash"] = generated_answer_relevancy_grade_hash

        return output_state

    def get_generated_answer_relevancy_grade_hash(
            self,
            question: str,
            generated_answer_hash: str,
    ) -> str:
        data: Dict[str, Any] = {
            "question": question,
            "generated_answer_hash": generated_answer_hash,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"generated_answer_relevancy_grade/{hashed_data}"

        return hashed_data

    def node_decide_transform_question_or_grade_answer_relevancy(self, input_state: LongFormQaGraphState) -> str:
        output_state: LongFormQaGraphState = input_state

        generated_hallucination_grade: str = input_state["generated_hallucination_grade"]
        if generated_hallucination_grade == "False":
            return "GRADE_ANSWER_RELEVANCY"

        transform_question_max_retry: int = input_state["transform_question_max_retry"]
        transform_question_current_retry: int = input_state["state"].transform_question_current_retry

        if transform_question_current_retry >= transform_question_max_retry:
            return "MAX_RETRY"

        output_state["state"].transform_question_current_retry += 1

        return "TRANSFORM_QUESTION"

    def node_decide_transform_question_or_provide_answer(self, input_state: LongFormQaGraphState) -> str:
        output_state: LongFormQaGraphState = input_state

        generated_answer_relevancy_grade: str = input_state["generated_answer_relevancy_grade"]
        if generated_answer_relevancy_grade == "True":
            return "PROVIDE_ANSWER"

        transform_question_max_retry: int = input_state["transform_question_max_retry"]
        transform_question_current_retry: int = input_state["state"].transform_question_current_retry
        if transform_question_current_retry >= transform_question_max_retry:
            return "MAX_RETRY"

        output_state["state"].transform_question_current_retry += 1

        return "TRANSFORM_QUESTION"

    async def node_transform_question(self, input_state: LongFormQaGraphState) -> LongFormQaGraphState:
        output_state: LongFormQaGraphState = input_state

        generated_question_hash: str = self.get_transformed_question_hash(
            question=input_state["question"]
        )
        existing_generated_question_hash: int = await self.two_datastore.async_client.exists(
            generated_question_hash
        )
        if existing_generated_question_hash == 0:
            is_generated_question_exist: bool = False
        elif existing_generated_question_hash == 1:
            is_generated_question_exist: bool = True
        else:
            raise use_case_exception.ExistingGeneratedQuestionHashInvalid()

        is_force_refresh_generated_question: bool = input_state["generator_setting"][
            "is_force_refresh_generated_question"]
        if is_generated_question_exist is False or is_force_refresh_generated_question is True:
            prompt: PromptTemplate = PromptTemplate(
                template="""
                <instruction>
                Converts the question to a better version that is optimized for vector store retrieval. Observe the question and try to reason about underlying semantics. Ensure the output is only the question without re-explain the instruction.
                <instruction/>
                <question>
                {question}
                <question/>
                """,
                input_variables=["question"]
            )
            text: str = prompt.format(
                question=input_state["question"]
            )
            messages: List[BaseMessage] = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                )
            ]
            llm_model: ChatLiteLLM = input_state["llm_setting"]["model"]
            chain: RunnableSerializable = llm_model | StrOutputParser()
            generated_question: str = await chain.ainvoke(
                input=messages
            )
            await self.two_datastore.async_client.set(
                name=generated_question_hash,
                value=generated_question.encode()
            )
        else:
            generated_question_byte: bytes = await self.two_datastore.async_client.get(
                generated_question_hash
            )
            generated_question: str = generated_question_byte.decode()

        output_state["question"] = generated_question
        output_state["generated_question_hash"] = generated_question_hash

        return output_state

    def get_transformed_question_hash(
            self,
            question: str,
    ) -> str:
        data: Dict[str, Any] = {
            "question": question,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"transformed_question/{hashed_data}"

        return hashed_data

    def compile(self) -> CompiledGraph:
        graph: StateGraph = StateGraph(LongFormQaGraphState)

        graph.add_node(
            node=self.node_get_llm_model.__name__,
            action=self.node_get_llm_model
        )
        graph.add_node(
            node=self.node_get_categorized_documents.__name__,
            action=self.node_get_categorized_documents
        )
        graph.add_node(
            node=self.node_embed.__name__,
            action=self.node_embed
        )
        graph.add_node(
            node=self.node_get_relevant_documents.__name__,
            action=self.node_get_relevant_documents
        )
        graph.add_node(
            node=self.node_get_re_ranked_documents.__name__,
            action=self.node_get_re_ranked_documents
        )
        graph.add_node(
            node=self.node_generate_answer.__name__,
            action=self.node_generate_answer
        )
        graph.add_node(
            node=self.node_grade_hallucination.__name__,
            action=self.node_grade_hallucination
        )
        graph.add_node(
            node=self.node_grade_answer_relevancy.__name__,
            action=self.node_grade_answer_relevancy
        )
        graph.add_node(
            node=self.node_transform_question.__name__,
            action=self.node_transform_question
        )

        graph.set_entry_point(
            key=self.node_get_llm_model.__name__
        )
        graph.add_edge(
            start_key=self.node_get_llm_model.__name__,
            end_key=self.node_get_categorized_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_get_categorized_documents.__name__,
            end_key=self.node_embed.__name__
        )
        graph.add_edge(
            start_key=self.node_embed.__name__,
            end_key=self.node_get_relevant_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_get_relevant_documents.__name__,
            end_key=self.node_get_re_ranked_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_get_re_ranked_documents.__name__,
            end_key=self.node_generate_answer.__name__
        )
        graph.add_edge(
            start_key=self.node_generate_answer.__name__,
            end_key=self.node_grade_hallucination.__name__
        )
        graph.add_conditional_edges(
            source=self.node_grade_hallucination.__name__,
            path=self.node_decide_transform_question_or_grade_answer_relevancy,
            path_map={
                "MAX_RETRY": END,
                "GRADE_ANSWER_RELEVANCY": self.node_grade_answer_relevancy.__name__,
                "TRANSFORM_QUESTION": self.node_transform_question.__name__
            }
        )
        graph.add_conditional_edges(
            source=self.node_grade_answer_relevancy.__name__,
            path=self.node_decide_transform_question_or_provide_answer,
            path_map={
                "MAX_RETRY": END,
                "PROVIDE_ANSWER": END,
                "TRANSFORM_QUESTION": self.node_transform_question.__name__
            }
        )
        graph.add_edge(
            start_key=self.node_transform_question.__name__,
            end_key=self.node_get_relevant_documents.__name__
        )

        compiled_graph: CompiledGraph = graph.compile()

        return compiled_graph
