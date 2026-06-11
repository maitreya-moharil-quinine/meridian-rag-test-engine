from fastapi import Request
from security.rate_limiter import is_rate_limited
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends

from security.auth import verify_api_key
from api.schema import QuestionRequest
from api.rag_service import RAGService

app = FastAPI(
    title="Meridian RAG API"
)

rag = RAGService()


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "vector_store_loaded": rag.retriever is not None
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    http_request: Request,
    api_key: str = Depends(verify_api_key)
):

    try:

        client_ip = http_request.client.host

        if is_rate_limited(client_ip):
            raise HTTPException(
                status_code=429,
                detail="To many requests.Please try again later."
            )
        
        return rag.ask(
            request.question,
            role="employee"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/store")
def store_vector_db(
    api_key: str = Depends(verify_api_key)
):

    try:

        result = rag.store()

        return {
            "status": "success",
            "message": "Knowledge Base Indexed Successfully",
            **result
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
