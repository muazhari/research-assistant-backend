import base64
import hashlib
import os
import re
from pathlib import Path
from typing import List

from txtmarker.factory import Factory

from apps.outers.settings.temp_datastore_setting import TempDatastoreSetting


class Annotater:

    def __init__(
            self,
            temp_datastore_setting: TempDatastoreSetting
    ):
        self.temp_datastore_setting: TempDatastoreSetting = temp_datastore_setting

    def annotate(
            self,
            labels: List[str],
            documents: List[str],
            input_file_data: bytes,
    ) -> bytes:
        input_file_name: str = f"annotater_input_{hashlib.md5(input_file_data).hexdigest()}"
        input_file_extension: str = ".pdf"
        input_file_path: Path = self.temp_datastore_setting.TEMP_DATASTORE_PATH / Path(
            f"{input_file_name}{input_file_extension}")
        output_file_name: str = f"annotater_output_{hashlib.md5(input_file_data).hexdigest()}"
        output_file_extension: str = ".pdf"
        output_file_path: Path = self.temp_datastore_setting.TEMP_DATASTORE_PATH / Path(
            f"/{output_file_name}{output_file_extension}")

        with open(input_file_path, "wb") as file:
            file.write(input_file_data)

        highlights = []
        for label, document in zip(labels, documents):
            highlight = (label, document)
            highlights.append(highlight)

        highlighter = Factory.create(
            extension="pdf",
            formatter=self.formatter,
            chunk=4
        )

        highlighter.highlight(
            infile=str(input_file_path),
            outfile=str(output_file_path),
            highlights=highlights
        )

        with open(output_file_path, "rb") as file:
            output_file_data = base64.b64encode(file.read())

        os.remove(input_file_path)
        os.remove(output_file_path)

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
