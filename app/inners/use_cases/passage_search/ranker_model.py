from haystack.nodes import SentenceTransformersRanker, BaseRanker

from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody


class RankerModel:
    def get_sentence_transformers_ranker(self, process_body: ProcessBody) -> BaseRanker:
        ranker: SentenceTransformersRanker = SentenceTransformersRanker(
            model_name_or_path=process_body.embedding_model.ranker_model,
        )
        return ranker

    def get_ranker(self, process_body: ProcessBody) -> BaseRanker:
        if process_body.ranker == "sentence_transformers":
            ranker = self.get_sentence_transformers_ranker(
                process_body=process_body
            )
        else:
            raise ValueError(f"Ranker {process_body.ranker} is not supported.")
        return ranker
