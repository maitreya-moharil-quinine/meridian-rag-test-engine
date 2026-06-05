from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings():
    """
    Create local embeddings using HuggingFace.
    No Google API required.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings
