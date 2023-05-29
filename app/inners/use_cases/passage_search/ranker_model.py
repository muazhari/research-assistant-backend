from haystack.nodes import SentenceTransformersRanker, BaseRanker

from app.inners.models.value_objects.contracts.requests.ranker_body import RankerBody


class RankerModel:
    def get_sentence_transformers_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        ranker: SentenceTransformersRanker = SentenceTransformersRanker(
            model_name_or_path=ranker_body.model,
        )
        return ranker

    def get_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        if ranker_body.source_type == "sentence_transformers":
            ranker = self.get_sentence_transformers_ranker(
                ranker_body=ranker_body
            )
        else:
            raise ValueError(f"Ranker Source Type {ranker_body.source_type} is not supported.")
        return ranker
