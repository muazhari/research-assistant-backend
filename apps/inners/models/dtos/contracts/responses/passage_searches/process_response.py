from datetime import datetime
from typing import List, Any, Dict

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class ProcessResponse(BaseResponse):
    re_ranked_documents: List[Dict[str, Any]]
    document_processes: List[DocumentProcess]
    final_document_urls: List[str]
    started_at: datetime
    finished_at: datetime
