# from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain_classic.retrievers import MultiQueryRetriever


def build_retriever(
    vector_store,
    llm,
    k: int = 5,
    lambda_mult: float = 0.5,
):
    """
    Build MultiQuery + MMR retriever once.
    """

    base_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "lambda_mult": lambda_mult,
        },
    )

    return MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
    )