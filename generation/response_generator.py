import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")

# 1. Increased max_output_tokens and slightly bumped temperature
LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,         
    max_output_tokens=2048   
)

# 2. Re-engineered prompt with formatting guidance for rich generation
PROMPT = PromptTemplate(
    template="""
        You are an expert assistant. Your goal is to provide deep, detailed, and comprehensive answers.

        Rules:
        1. Use ONLY the provided context to answer the question.
        2. Provide an exhaustive, fully fleshed-out explanation based on that context. Do not give short or brief summaries.
        3. Break down complex points step-by-step using descriptive paragraphs and structured bullet points where applicable.
        4. If the answer is not present in the context at all, say: "I could not find that information in the knowledge base."

        Context:
        {context}

        Question:
        {question}

        Detailed Answer:
        """,
    input_variables=["context", "question"]
)

def generate_response(question, retrieved_docs):

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    print("Retrieved context length:", len(context))
    print("Question:", question)

    return "DEBUG: Retrieval completed successfully."
