from langchain_community.vectorstores import FAISS

def save_vector_store(vector_store):

    vector_store.save_local(
        "vector_db"
    )


# def load_vector_store(embeddings):

#     return FAISS.load_local(
#         "vector_db",
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

def store_vectors(chunks, embeddings):
    """
    Create FAISS vector store.

    Args:
        chunks: Output from split_documents()
        embeddings: Output from create_embeddings()

    Returns:
        FAISS vector store
    """

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store
