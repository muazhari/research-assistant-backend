from datetime import datetime
from typing import List, Any, Dict

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class ReRankedDocumentMetadata(BaseResponse):
    document_id: str
    relevancy_score: float
    re_ranked_score: float
    origin_metadata: List[Dict[str, Any]]


class ReRankedDocument(BaseResponse):
    page_content: str
    metadata: ReRankedDocumentMetadata


class ProcessResponse(BaseResponse):
    re_ranked_documents: List[ReRankedDocument]
    document_processes: List[DocumentProcess]
    final_document_urls: List[str]
    started_at: datetime
    finished_at: datetime
