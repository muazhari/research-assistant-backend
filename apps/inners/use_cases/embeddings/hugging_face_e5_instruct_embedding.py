from typing import Any, List

from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings


class HuggingFaceE5InstructEmbeddings(HuggingFaceEmbeddings):
    query_instruction: str

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def _get_detailed_instruct(self, task_description: str, query: str) -> str:
        return f'Instruct: {task_description}\nQuery: {query}'

    def embed_query(self, text: str) -> List[float]:
        instructed_text = self._get_detailed_instruct(self.query_instruction, text)
        return self.embed_documents(texts=[instructed_text])[0]
