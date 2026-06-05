from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """
    Split loaded documents into chunks.

    Args:
        documents: Output from load_documents()
        chunk_size: Max chunk size
        chunk_overlap: Overlap between chunks

    Returns:
        List[Document]
    """

    langchain_docs = [
        Document(
            page_content=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in documents
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(langchain_docs)

    return chunks