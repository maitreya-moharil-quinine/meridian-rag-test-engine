from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import create_embeddings

from ingestion.vector_store import (
    store_vectors,
    save_vector_store
)

from retrieval.retriever import build_retriever

from generation.response_generator import (
    generate_response,
    LLM
)


class RAGService:

    def __init__(self):

        self.embeddings = None
        self.vector_store = None
        self.retriever = None

    def store(self):
        """
        Build FAISS index from knowledge_base,
        save it locally,
        and load it into memory.
        """

        documents = load_documents(
            "knowledge_base"
        )

        chunks = split_documents(
            documents
        )

        self.embeddings = create_embeddings()

        self.vector_store = store_vectors(
            chunks,
            self.embeddings
        )

        save_vector_store(
            self.vector_store
        )

        self.retriever = build_retriever(
            vector_store=self.vector_store,
            llm=LLM
        )

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }

    def ask(self, question: str):

        if self.retriever is None:
            raise RuntimeError(
                "Knowledge base not initialized. Run /store first."
            )

        docs = self.retriever.invoke(
            question
        )

        answer = generate_response(
            question,
            docs
        )

        return {
            "answer": answer,
            "sources": list(
                set(
                    doc.metadata.get(
                        "file_name",
                        "Unknown"
                    )
                    for doc in docs
                )
            )
        }

    def health(self):

        return {
            "status": "healthy",
            "knowledge_base_loaded": (
                self.retriever is not None
            )
        }
