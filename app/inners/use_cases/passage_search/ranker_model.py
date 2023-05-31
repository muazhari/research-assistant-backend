from haystack.nodes import SentenceTransformersRanker, BaseRanker

from app.inners.models.value_objects.contracts.requests.basic_settings.ranker_body import RankerBody


class RankerModel:
    def get_sentence_transformers_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        ranker: SentenceTransformersRanker = SentenceTransformersRanker(
            model_name_or_path=ranker_body.model,
            top_k=ranker_body.top_k,
        )
        return ranker

    def get_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        if ranker_body.source_type == "sentence_transformers":
            ranker = self.get_sentence_transformers_ranker(
                ranker_body=ranker_body,
            )
        else:
            raise NotImplementedError(f"Ranker Source Type {ranker_body.source_type} is not supported.")
        return ranker
