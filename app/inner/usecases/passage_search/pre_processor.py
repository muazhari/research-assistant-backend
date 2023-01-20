from typing import List, Tuple, Optional, Any

import more_itertools
from txtai.pipeline import Textractor, Segmentation


class PreProcessor:

    def segment(self, corpus, granularity) -> List[str]:
        granularized_corpus = None
        if (granularity == "sentence"):
            segmentator = Segmentation(sentences=True)
            granularized_corpus = segmentator(text=corpus)
        elif granularity == "paragraph":
            segmentator = Segmentation(paragraphs=True)
            granularized_corpus = segmentator(text=corpus)
        elif granularity == "word":
            granularized_corpus = corpus.split(" ")
        else:
            raise ValueError("Granularity not supported.")
        return granularized_corpus

    def textract(self, corpus, granularity) -> List[str]:
        granularized_corpus = None
        if granularity == "word":
            granularized_corpus = corpus.split(" ")
        elif granularity == "sentence":
            textractor = Textractor(sentences=True)
            granularized_corpus = textractor(text=corpus)
        elif granularity == "paragraph":
            textractor = Textractor(paragraphs=True)
            granularized_corpus = textractor(text=corpus)
        else:
            ValueError(f"Granularity {granularity} is not supported.")
        return granularized_corpus

    def granularize(self, corpus, source_type, granularity) -> List[str]:
        granularized_corpus = None
        if source_type in ["text"]:
            granularized_corpus = self.segment(corpus, granularity)
        elif source_type in ["file", "web"]:
            granularized_corpus = self.textract(corpus, granularity)
        else:
            raise ValueError(f"Source type {source_type} is not supported.")
        return granularized_corpus

    def degranularize(self, corpus, granularity_source) -> str:
        degranularized_corpus = None
        if granularity_source == "word":
            degranularized_corpus = " ".join(corpus)
        elif granularity_source == "sentence":
            degranularized_corpus = ". ".join(corpus)
        elif granularity_source == "paragraph":
            degranularized_corpus = "\n".join(corpus)
        else:
            ValueError(f"Granularity source {granularity_source} is not supported.")
        return degranularized_corpus

    def windowize(self, corpus, window_size) -> List[Tuple[str, ...]]:
        return list(more_itertools.windowed(corpus, window_size))

    def process(self, corpus, source_type, granularity, window_size):
        granularized_corpus = self.granularize(corpus, source_type, granularity)
        windowed_granularized_corpus = self.windowize(granularized_corpus, window_size)
        return windowed_granularized_corpus


pre_processor = PreProcessor()
