from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends

from security.auth import verify_api_key
from api.schema import (QuestionRequest)
from api.rag_service import (RAGService)

app = FastAPI(
    title="Meridian RAG API"
)

rag = RAGService()

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "vector_store_loaded":
        rag.retriever is not None
    }

@app.post("/store")
def store_vector_db(
    auth=Depends(verify_api_key)
):

    try:

        result = rag.store()

        return {
            "status": "success",
            "message": "Knowledge Base Indexed Successfully",
            **result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    auth=Depends(verify_api_key)
):

    try:

        return rag.ask(
            request.question
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
