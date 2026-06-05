import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path

# Find the absolute path to the root folder (MERIDIAN)
# This looks up 2 levels from embedder.py (ingestion/ -> MERIDIAN/)
root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / ".env"

# Explicitly load the .env from the precise absolute path
load_dotenv(dotenv_path=env_path)

def create_embeddings():
    """
    Creates cloud-based Google GenAI embeddings using an explicit API key.
    """
    # 2. Fetch the key from the environment
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    # 3. Defensive check to catch configuration bugs early
    if not api_key:
        raise ValueError(
            "CRITICAL: GOOGLE_API_KEY is missing from your environment. "
            "Please check that your .env file exists in the root folder."
        )
    
    # 4. Explicitly pass the api_key to override Pydantic checks
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=api_key  # Passing it explicitly resolves the validation error
    )
    
    return embeddings
