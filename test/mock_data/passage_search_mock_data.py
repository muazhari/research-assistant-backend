import pathlib
import uuid

from app.inners.models.entities.account import Account
from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.entities.file_document import FileDocument
from app.inners.models.entities.text_document import TextDocument
from app.inners.models.entities.web_document import WebDocument


class PassageSearchMockData:

    def __init__(self):
        self.account_data = [
            Account(
                id=uuid.uuid4(),
                name="name0",
                email="email0",
                password="password0",
            ),
        ]

        self.document_type_data = [
            DocumentType(
                id=uuid.uuid4(),
                name="file",
                description="description0"
            ),
            DocumentType(
                id=uuid.uuid4(),
                name="text",
                description="description1"
            ),
            DocumentType(
                id=uuid.uuid4(),
                name="web",
                description="description2"
            ),
        ]

        self.document_data = [
            Document(
                id=uuid.uuid4(),
                name="name2",
                description="description2",
                document_type_id=self.document_type_data[0].id,
                account_id=self.account_data[0].id,
            ),
        ]

        file_path = pathlib.Path("../../test/mock_data/files/Artificial_Intelligence_in_Education_A_Review.pdf")
        with open(file_path, "rb") as file:
            file_bytes = file.read()

        self.file_document_data = [
            FileDocument(
                id=uuid.uuid4(),
                document_id=self.document_data[0].id,
                file_name=file_path.name,
                file_extension=file_path.suffix,
                file_bytes=file_bytes,
            )
        ]

        self.text_document_data = [
            TextDocument(
                id=uuid.uuid4(),
                document_id=self.document_data[0].id,
                text_content="""Software engineering is an engineering-based approach to software development.[1][2][3] A software engineer is a person who applies the engineering design process to design, develop, maintain, test, and evaluate computer software. The term programmer is sometimes used as a synonym, but may also refer more to implementation rather than design and can also lack connotations of engineering education or skills.[4]

Engineering techniques are used to inform the software development process,[1][5] which involves the definition, implementation, assessment, measurement, management, change, and improvement of the software life cycle process itself. It heavily uses software configuration management,[1][5] which is about systematically controlling changes to the configuration, and maintaining the integrity and traceability of the configuration and code throughout the system life cycle. Modern processes use software versioning."""
            )
        ]

        self.web_document_data = [
            WebDocument(
                id=uuid.uuid4(),
                document_id=self.document_data[0].id,
                web_url="https://en.wikipedia.org/wiki/Software_engineering"
            )
        ]
