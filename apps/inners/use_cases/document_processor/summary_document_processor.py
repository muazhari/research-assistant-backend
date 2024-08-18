from typing import List

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from unstructured.documents.elements import Table, Image


class SummaryDocumentProcessor:

    async def summarize_tables(self, tables: List[Table], llm_model: ChatLiteLLM) -> List[str]:
        prompt: PromptTemplate = PromptTemplate(
            template="""
            <instruction>
            Give a concise passage summary of the table that is well optimized for retrieval. These summary will be embedded and used to retrieve the table. Ensure the output does not re-explain the instruction.
            <instruction/>
            <table>
            {table}
            <table/>
            """,
            input_variables=["table"]
        )

        batch_messages: List[List[BaseMessage]] = []
        for table in tables:
            text: str = prompt.format(
                table=table.text
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
            batch_messages.append(messages)

        chain: RunnableSerializable = llm_model | StrOutputParser()
        generated_summaries: List[str] = await chain.abatch(
            inputs=batch_messages
        )

        return generated_summaries

    async def summarize_images(self, images: List[Image], llm_model: ChatLiteLLM) -> List[str]:
        prompt = """Instruction: Give a concise passage summary of the image that is well optimized for retrieval. These summary will be embedded and used to retrieve the image. Ensure the output does not re-explain the instruction.
        Image:"""
        batch_messages: List[List[BaseMessage]] = []
        for image in images:
            messages: List[BaseMessage] = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{image.metadata.image_mime_type};base64,{image.metadata.image_base64}",
                            }
                        }
                    ]
                )
            ]
            batch_messages.append(messages)

        chain: RunnableSerializable = llm_model | StrOutputParser()
        generated_summaries: List[str] = await chain.abatch(
            inputs=batch_messages
        )

        return generated_summaries
