import base64
from pathlib import Path

import pdfkit
from pdfrw import PdfReader, PdfWriter

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType


class DocumentConversionUtility:
    def __init__(self):
        self.options = {
            'page-size': 'Letter',
            'margin-top': '0.25in',
            'margin-right': '1.00in',
            'margin-bottom': '0.25in',
            'margin-left': '1.00in',
        }

    def text_to_pdf(self, text: str) -> bytes:
        return base64.b64encode(pdfkit.from_string(text, options=self.options))

    def web_to_pdf(self, url: str) -> bytes:
        return base64.b64encode(pdfkit.from_url(url, options=self.options))

    def file_to_pdf(self, input_file_path: Path) -> bytes:
        with open(input_file_path, "rb") as file:
            input_file_bytes = base64.b64encode(file.read())
            if input_file_path.suffix == ".pdf":
                return input_file_bytes
            else:
                raise NotImplementedError(f"File type {input_file_path.suffix} is not supported.")

    def corpus_to_pdf(self, corpus: str, document: Document, document_type: DocumentType) -> bytes:
        if document_type.name == "text":
            output = self.text_to_pdf(text=corpus)
        elif document_type.name == "file":
            output = self.file_to_pdf(input_file_path=Path(corpus))
        elif document_type.name == "web":
            output = self.web_to_pdf(url=corpus)
        else:
            raise NotImplementedError(f"Document type {document_type.name} is not supported.")

        return output

    def split_pdf_page(self, start_page: int, end_page: int, input_file_path: Path, output_file_path: Path) -> Path:
        """
            This method has a side effect of creating a file in the output_file_path.
        """

        input_pdf_reader = PdfReader(input_file_path)
        output_pdf_writer = PdfWriter(output_file_path)
        output_pdf_writer.addpages(input_pdf_reader.pages[start_page - 1:end_page])
        output_pdf_writer.write()

        return output_file_path

    def file_bytes_to_pdf(self, file_bytes: bytes, output_file_path: Path) -> Path:
        with open(output_file_path, "wb") as file:
            file.write(file_bytes)

        return output_file_path

    def get_pdf_page_length(self, input_file_path: Path) -> int:
        input_pdf_reader = PdfReader(input_file_path)
        pdf_page_length = len(input_pdf_reader.pages)

        return pdf_page_length
