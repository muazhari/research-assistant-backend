import re
import uuid
from pathlib import Path
from typing import List, Tuple
from uuid import UUID

from magic import Magic
from txtmarker.factory import Factory

from apps.inners.exceptions import use_case_exception
from apps.outers.repositories.file_document_repository import FileDocumentRepository


class MarkerDocumentConverter:
    def __init__(
            self,
            file_document_repository: FileDocumentRepository,
    ):
        self.file_document_repository = file_document_repository
        self.file_path: Path = self.file_document_repository.file_path / "marker_converted_documents"
        self.file_path.mkdir(exist_ok=True)

    async def convert_from_data(self, input_file_data: bytes, highlights: List[Tuple[str, str]]) -> bytes:
        magic: Magic = Magic(mime=True)
        mime_type: str = magic.from_buffer(input_file_data)
        if mime_type != "application/pdf":
            raise use_case_exception.DocumentTypeNotSupported()

        id: UUID = uuid.uuid4()
        input_file_path: Path = self.file_path / f"unconverted_{id}.pdf"
        self.file_document_repository.save_file(
            relative_file_path=Path(input_file_path.parent.name) / input_file_path.name,
            file_data=input_file_data
        )
        highlighter = Factory.create(
            extension="pdf",
            formatter=self.formatter,
            chunk=4
        )
        output_file_path: Path = self.file_path / f"converted_{id}.pdf"
        highlighter.highlight(
            infile=str(input_file_path),
            outfile=str(output_file_path),
            highlights=highlights
        )
        output_file_data: bytes = self.file_document_repository.read_file_data(
            relative_file_path=Path(output_file_path.parent.name) / output_file_path.name
        )
        self.file_document_repository.remove_file(
            relative_file_path=Path(input_file_path.parent.name) / input_file_path.name
        )
        self.file_document_repository.remove_file(
            relative_file_path=Path(output_file_path.parent.name) / output_file_path.name
        )

        return output_file_data

    def formatter(self, text):
        """
        Custom formatter that is passed to PDF Annotation method. This logic maps data cleansing logic in paperetl.

        Reference: https://github.com/neuml/paperetl/blob/master/src/python/paperetl/text.py

        Args:
            text: input text

        Returns:
            clean text
        """

        # List of patterns
        patterns = []

        # Remove emails
        patterns.append(r"\w+@\w+(\.[a-z]{2,})+")

        # Remove urls
        patterns.append(r"http(s)?\:\/\/\S+")

        # Remove single characters repeated at least 3 times (ex. j o u r n a l)
        patterns.append(r"(^|\s)(\w\s+){3,}")

        # Remove citations references (ex. [3] [4] [5])
        patterns.append(r"(\[\d+\]\,?\s?){3,}(\.|\,)?")

        # Remove citations references (ex. [3, 4, 5])
        patterns.append(r"\[[\d\,\s]+\]")

        # Remove citations references (ex. (NUM1) repeated at least 3 times with whitespace
        patterns.append(r"(\(\d+\)\s){3,}")

        # Build regex pattern
        pattern = re.compile("|".join([f"({p})" for p in patterns]))

        # Clean/transform text
        text = pattern.sub(" ", text)

        # Remove extra spacing either caused by replacements or already in text
        text = re.sub(r" {2,}|\.{2,}", " ", text)

        # Limit to alphanumeric characters
        text = re.sub(r"[^A-Za-z0-9]", "", text)

        return text
