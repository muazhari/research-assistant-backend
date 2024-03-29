import concurrent.futures
import math
import os
from pathlib import Path
from typing import List, Tuple

import more_itertools
import psutil
from haystack import Document as HaystackDocument
from txtai.pipeline import Segmentation, Textractor

from app.inners.use_cases.utilities.document_conversion_utility import DocumentConversionUtility
from app.outers.settings.temp_datastore_setting import TempDatastoreSetting


class DocumentProcessorUtility:

    def __init__(
            self,
            document_conversion_utility: DocumentConversionUtility,
            temp_datastore_setting: TempDatastoreSetting
    ):
        self.document_conversion_utility: DocumentConversionUtility = document_conversion_utility
        self.temp_datastore_setting: TempDatastoreSetting = temp_datastore_setting

    def segment(self, corpus: str, granularity: str) -> List[str]:
        granularized_corpus: List[str] = []
        if (granularity == "sentence"):
            segmentator = Segmentation(sentences=True)
            granularized_corpus = segmentator(text=corpus)
        elif granularity == "paragraph":
            segmentator = Segmentation(paragraphs=True)
            granularized_corpus = segmentator(text=corpus)
        elif granularity == "word":
            granularized_corpus = corpus.split(" ")
        else:
            NotImplementedError(f"Granularity {granularity} is not supported.")

        return granularized_corpus

    def textract(self, corpus: str, granularity: str) -> List[str]:
        granularized_corpus: List[str] = []
        if granularity == "word":
            textractor = Textractor()
            granularized_corpus = textractor(text=corpus).split(" ")
        elif granularity == "sentence":
            textractor = Textractor(sentences=True)
            granularized_corpus = textractor(text=corpus)
        elif granularity == "paragraph":
            textractor = Textractor(paragraphs=True)
            granularized_corpus = textractor(text=corpus)
        else:
            NotImplementedError(f"Granularity {granularity} is not supported.")

        return granularized_corpus

    def granularize(self, corpus: str, corpus_source_type: str, granularity: str) -> List[str]:
        if corpus_source_type in ["text"]:
            granularized_corpus = self.segment(corpus, granularity)
        elif corpus_source_type in ["file"]:
            page_size = self.document_conversion_utility.get_pdf_page_length(input_file_path=Path(corpus))
            core_size = math.floor(psutil.cpu_count(logical=False) / 2)
            chunk_size = math.ceil(page_size / core_size)
            split_pdf_page_args = []
            for i, j in zip(range(0, page_size, chunk_size), range(chunk_size, page_size + chunk_size, chunk_size)):
                start_page = i + 1
                end_page = min(j, page_size)
                input_file_path = Path(corpus)
                input_file_path_base = input_file_path.stem
                output_file_path = self.temp_datastore_setting.TEMP_DATASTORE_PATH / Path(
                    f"{input_file_path_base}_chunk_{start_page}_to_{end_page}.pdf")
                split_pdf_page_arg = (start_page, end_page, input_file_path, output_file_path)
                split_pdf_page_args.append(split_pdf_page_arg)

            with concurrent.futures.ProcessPoolExecutor(max_workers=core_size) as executor:
                output_file_paths = list(executor.map(
                    self.document_conversion_utility.split_pdf_page,
                    *zip(*split_pdf_page_args)
                ))
                textract_args = [
                    (str(split_pdf_page_arg[3]), granularity) for split_pdf_page_arg in split_pdf_page_args
                ]
                textract_result = list(executor.map(self.textract, *zip(*textract_args)))
                granularized_corpus = [item for sublist in textract_result for item in sublist]
                executor.map(os.remove, output_file_paths)
        elif corpus_source_type in ["web"]:
            granularized_corpus = self.textract(corpus, granularity)
        else:
            raise NotImplementedError(f"Source type {corpus_source_type} is not supported.")
        return granularized_corpus

    def windowize(self, corpus: List[str], window_size: int) -> List[Tuple[str, ...]]:
        if window_size > len(corpus):
            raise ValueError(f"Window size {window_size} is greater than corpus size {len(corpus)}.")

        return list(more_itertools.windowed(corpus, window_size))

    def degranularize(self, windowed_corpus: Tuple[str], granularity_source: str) -> str:
        degranularized_corpus = None
        if granularity_source in ["word", "sentence"]:
            degranularized_corpus = " ".join(windowed_corpus)
        elif granularity_source in ["paragraph"]:
            degranularized_corpus = "\n".join(windowed_corpus)
        else:
            NotImplementedError(f"Granularity {granularity_source} is not supported.")
        return degranularized_corpus

    def prefixer(self, documents: List[HaystackDocument], prefix: str) -> List[HaystackDocument]:
        prefixed_documents: List[HaystackDocument] = []
        for document in documents:
            prefixed_document: HaystackDocument = HaystackDocument(
                id=document.id,
                content=prefix + document.content,
                content_type=document.content_type,
                meta=document.meta,
                score=document.score
            )
            prefixed_documents.append(prefixed_document)

        return prefixed_documents

    def deprefixer(self, documents: List[HaystackDocument], prefix: str) -> List[HaystackDocument]:
        deprefixed_documents: List[HaystackDocument] = []
        for document in documents:
            deprefixed_document: HaystackDocument = HaystackDocument(
                id=document.id,
                content=document.content[len(prefix):],
                content_type=document.content_type,
                meta=document.meta,
                score=document.score
            )
            deprefixed_documents.append(deprefixed_document)

        return deprefixed_documents

    def process(self, corpus: str, corpus_source_type: str, granularity: str,
                window_sizes: List[int], prefix: str) -> List[HaystackDocument]:
        granularized_corpus: List[str] = self.granularize(corpus, corpus_source_type, granularity)

        documents_with_many_window_size = []
        for window_size in window_sizes:
            windowed_corpus: List[Tuple[str, ...]] = self.windowize(granularized_corpus, window_size)
            for index_window, content_window in enumerate(windowed_corpus):
                document: HaystackDocument = HaystackDocument(
                    content=self.degranularize(content_window, granularity),
                    meta={"index_window": index_window, "window_size": window_size}
                )
                documents_with_many_window_size.append(document)

        prefixed_documents: List[HaystackDocument] = self.prefixer(documents_with_many_window_size, prefix)

        return prefixed_documents
