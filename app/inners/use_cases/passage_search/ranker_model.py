from haystack.nodes import SentenceTransformersRanker, BaseRanker, CohereRanker

from app.inners.models.value_objects.contracts.requests.basic_settings.ranker_body import RankerBody


class RankerModel:
    def get_sentence_transformers_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        ranker: SentenceTransformersRanker = SentenceTransformersRanker(
            model_name_or_path=ranker_body.ranker_model.model,
            top_k=ranker_body.top_k,
        )
        return ranker

    def get_online_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        ranker: CohereRanker = CohereRanker(
            model_name_or_path=ranker_body.ranker_model.model,
            api_key=ranker_body.ranker_model.api_key,
            top_k=ranker_body.top_k,
        )
        return ranker

    def get_ranker(self, ranker_body: RankerBody) -> BaseRanker:
        if ranker_body.source_type == "sentence_transformers":
            ranker = self.get_sentence_transformers_ranker(
                ranker_body=ranker_body,
            )
        elif ranker_body.source_type == "online":
            ranker = self.get_online_ranker(
                ranker_body=ranker_body,
            )
        else:
            raise NotImplementedError(f"Ranker source type {ranker_body.source_type} is not supported.")
        return ranker
