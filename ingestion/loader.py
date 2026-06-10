from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx"
}


def _extract_text(file_path: Path) -> str:

    suffix = file_path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    if suffix == ".pdf":
        reader = PdfReader(str(file_path))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if suffix == ".docx":
        doc = Document(str(file_path))

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

    return ""


def get_document_type(file_name: str) -> str:
    """
    Assign document category based on filename.
    Used later for RBAC.
    """

    file_name = file_name.lower()

    if "leave" in file_name:
        return "leave_policy"

    elif "salary" in file_name:
        return "salary_data"

    elif "employee" in file_name:
        return "employee_data"

    elif "hr" in file_name:
        return "hr_document"

    else:
        return "company_policy"


def load_documents(folder_path: str) -> List[Dict]:
    """
    Load documents from knowledge base.
    """

    documents = []

    for file_path in Path(folder_path).rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:

            text = _extract_text(file_path)

            if not text.strip():
                continue

            document_type = get_document_type(
                file_path.name
            )

            documents.append(
                {
                    "content": text,
                    "metadata": {
                        "source": str(file_path),
                        "file_name": file_path.name,
                        "file_type": file_path.suffix.lower(),
                        "document_type": document_type
                    }
                }
            )

        except Exception as e:

            print(
                f"Failed to load {file_path}: {e}"
            )

    return documents
