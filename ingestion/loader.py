from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}

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

def load_documents(folder_path: str) -> List[Dict]:
    """
    Load documents from a knowledge base folder.

    Returns:
        [
            {
                "content": "...",
                "metadata": {
                    "source": "knowledge_base/file.pdf",
                    "file_name": "file.pdf",
                    "file_type": ".pdf"
                }
            }
        ]
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

            documents.append(
                {
                    "content": text,
                    "metadata": {
                        "source": str(file_path),
                        "file_name": file_path.name,
                        "file_type": file_path.suffix.lower(),
                    },
                }
            )

        except Exception as e:
            print(f"Failed to load {file_path}: {e}")

    return documents
