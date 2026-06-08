# from ingestion.vector_store import load_vector_store
# from ingestion.embedder import create_embeddings
# from langchain_community.vectorstores import FAISS
# from retrieval.retriever import build_retriever
# from generation.response_generator import (
#     generate_response,
#     LLM
# )

# embeddings = create_embeddings()

# vector_store = load_vector_store(embeddings)

# retriever = build_retriever(
#     vector_store=vector_store,
#     llm=LLM
# )

# while True:

#     question = input("\nAsk: ")

#     if question.lower() in [
#         "exit",
#         "quit",
#     ]:
#         break

#     docs = retriever.invoke(question)

#     answer = generate_response(
#         question,
#         docs
#     )

#     print("\nAnswer:\n")
#     print(answer)
