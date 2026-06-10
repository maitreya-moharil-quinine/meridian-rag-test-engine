from security.access_control import has_access
from security.logger import log_event
from security.prompt_guard import detect_prompt_injection
from security.data_guard import contains_sensitive_request

from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.embedder import create_embeddings

from ingestion.vector_store import (
    store_vectors,
    save_vector_store,
    load_vector_store
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

        try:

            self.embeddings = create_embeddings()

            self.vector_store = load_vector_store(
                self.embeddings
            )

            self.retriever = build_retriever(
                vector_store=self.vector_store,
                llm=LLM
            )

            print("✅ Existing FAISS index loaded")

        except Exception as e:

            print("⚠️ No existing FAISS index found")
            print(e)

    def store(self):
        """
        Build vector database from knowledge base.
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

    def ask(
        self,
        question: str,
        role: str = "employee"
    ):

        if self.retriever is None:
            raise RuntimeError(
                "Knowledge base not initialized. Run /store first."
            )

        # Prompt Injection Protection
        if detect_prompt_injection(question):

            log_event(
                "PROMPT_INJECTION",
                question,
                "BLOCKED"
            )

            raise RuntimeError(
                "Potential prompt injection detected."
            )

        # Sensitive Data Protection
        if contains_sensitive_request(question):

            log_event(
                "SENSITIVE_DATA",
                question,
                "BLOCKED"
            )

            raise RuntimeError(
                "Access denied: sensitive information request detected."
            )

        docs = self.retriever.invoke(
            question
        )

        # RBAC Filtering
        filtered_docs = []

        for doc in docs:

            document_type = doc.metadata.get(
                "document_type",
                "company_policy"
            )

            if has_access(
                role,
                document_type
            ):
                filtered_docs.append(doc)

        if not filtered_docs:

            raise RuntimeError(
                "Access denied."
            )

        answer = generate_response(
            question,
            filtered_docs
        )

        log_event(
            "QUESTION",
            question,
            "ALLOWED"
        )

        return {
            "answer": answer,
            "sources": list(
                set(
                    doc.metadata.get(
                        "file_name",
                        "Unknown"
                    )
                    for doc in filtered_docs
                )
            )
        }

    def health(self):

        return {
            "status": "healthy",
            "knowledge_base_loaded":
            self.retriever is not None
        }