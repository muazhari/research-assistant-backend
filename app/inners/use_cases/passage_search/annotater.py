import hashlib
import os
import re
from pathlib import Path
from typing import List

from txtmarker.factory import Factory

from app.inners.use_cases.utilities.locker import Locker


class Annotater:

    @Locker.wait_lock
    def annotate(self,
                 labels: List[str],
                 documents: List[str], input_file_bytes: bytes,
                 overwrite: bool = True
                 ) -> bytes:
        input_file_name: str = f"annotater_input_{hashlib.md5(input_file_bytes).hexdigest()}"
        input_file_extension: str = ".pdf"
        input_file_path: Path = Path(f"app/outers/persistences/temps/{input_file_name}{input_file_extension}")
        output_file_name: str = f"annotater_output_{hashlib.md5(input_file_bytes).hexdigest()}"
        output_file_extension: str = ".pdf"
        output_file_path: Path = Path(f"app/outers/persistences/temps/{output_file_name}{output_file_extension}")

        if os.path.exists(output_file_path):
            if overwrite is False:
                with open(output_file_path, "rb") as file:
                    output_file_bytes = file.read()
                return output_file_bytes

        with open(input_file_path, "wb") as file:
            file.write(input_file_bytes)

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
            output_file_bytes = file.read()

        return output_file_bytes

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
