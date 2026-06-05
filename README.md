# meridian-rag-test-engine
This Repository contains everything related to Testing RAG System for QCS Framework

# Building RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system using:

* LangChain
* FAISS Vector Store
* BAAI/bge-m3 Embedding Model
* Google Gemini 2.5 Flash
* FastAPI

The system enables users to upload a knowledge base consisting of documents and query that knowledge base through natural language questions.

The architecture follows a modular design where ingestion, retrieval, generation, and API layers are separated for maintainability and scalability.

---

# Project Structure

```text
rag_system/
│
├── knowledge_base/
│   ├── *.pdf
│   ├── *.docx
│   ├── *.txt
│   └── *.md
│
├── vector_db/
│   ├── index.faiss
│   └── index.pkl
│
├── ingestion/
│   ├── loader.py
│   ├── splitter.py
│   ├── embedder.py
│   └── vector_store.py
│
├── retrieval/
│   └── retriever.py
│
├── generation/
│   └── response_generator.py
│
├── api/
│   ├── app.py
│   ├── schemas.py
│   └── rag_service.py
│
└── .env
```

---

# Components

## Document Loader

Responsible for reading documents from the knowledge base.

Supported formats:

* PDF
* DOCX
* TXT
* MD

Output:

```python
[
    {
        "content": "...",
        "metadata": {
            "file_name": "atlas.pdf",
            "source": "knowledge_base/atlas.pdf"
        }
    }
]
```

---

## Document Splitter

Uses:

```python
RecursiveCharacterTextSplitter
```

Purpose:

* Break large documents into manageable chunks
* Improve retrieval accuracy
* Maintain semantic context through chunk overlap

Output:

```python
List[Document]
```

---

## Embedding Generator

Embedding Model:

```text
BAAI/bge-m3
```

Purpose:

* Convert text chunks into vector representations
* Enable semantic similarity search

Configuration:

```python
normalize_embeddings=True
```

---

## Vector Store

Vector Database:

```text
FAISS
```

Purpose:

* Store chunk embeddings
* Enable fast similarity search
* Persist indexes locally

Generated Files:

```text
vector_db/
├── index.faiss
└── index.pkl
```

---

## Retriever

Retrieval Strategy:

```text
MultiQueryRetriever + MMR
```

### MultiQueryRetriever

Generates multiple variations of the user's question to improve recall.

Example:

User Query:

```text
What is MITRE ATLAS?
```

Generated Queries:

```text
Explain MITRE ATLAS
Overview of MITRE ATLAS
Purpose of MITRE ATLAS
MITRE ATLAS framework
```

---

### MMR (Max Marginal Relevance)

Balances:

* Relevance
* Diversity

This reduces duplicate chunks and increases information coverage.

---

## Response Generator

LLM:

```text
Gemini 2.5 Flash
```

Responsibilities:

* Consume retrieved context
* Generate detailed responses
* Restrict responses to retrieved knowledge base content

Prompt Guardrail:

```text
Use ONLY the provided context.
```

This reduces hallucinations and ensures answers remain grounded in the knowledge base.

---

# API Endpoints

## POST /store

Builds and loads the knowledge base.

### Responsibilities

* Load documents
* Split documents
* Generate embeddings
* Create FAISS index
* Save FAISS index locally
* Load retriever into memory

### Request

No request body required.

### Response

```json
{
  "status": "success",
  "message": "Knowledge Base Indexed Successfully",
  "documents": 10,
  "chunks": 350
}
```

---

## POST /ask

Query the knowledge base.

### Request

```json
{
  "question": "What is MITRE ATLAS?"
}
```

### Response

```json
{
  "answer": "...",
  "sources": [
    "atlas.pdf",
    "security.md"
  ]
}
```

---

## GET /health

Check service health.

### Response

```json
{
  "status": "healthy",
  "knowledge_base_loaded": true
}
```

---

# User Flow

## Step 1: Add Documents

Place documents inside:

```text
knowledge_base/
```

Example:

```text
knowledge_base/
├── atlas.pdf
├── security.md
├── policies.docx
└── notes.txt
```

---

## Step 2: Build Knowledge Base

Call:

```http
POST /store
```

This creates:

```text
vector_db/
├── index.faiss
└── index.pkl
```

and loads the retriever into memory.

---

## Step 3: Ask Questions

Call:

```http
POST /ask
```

with a question.

Example:

```json
{
  "question": "Explain MITRE ATLAS attack techniques."
}
```

---

## Step 4: Receive Grounded Response

The system:

* Retrieves relevant chunks
* Generates a response using Gemini
* Returns supporting source files

---

# Data Flow

## Knowledge Base Ingestion Flow

```text
knowledge_base/
        │
        ▼
load_documents()
        │
        ▼
split_documents()
        │
        ▼
create_embeddings()
        │
        ▼
store_vectors()
        │
        ▼
save_vector_store()
        │
        ▼
vector_db/
```

---

## Query Flow

```text
User Question
        │
        ▼
/ask
        │
        ▼
MultiQueryRetriever
        │
        ▼
MMR Retrieval
        │
        ▼
Relevant Chunks
        │
        ▼
Prompt Construction
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Final Answer
```

---

# Retrieval-Augmented Generation Lifecycle

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Embedding
    │
    ▼
FAISS Index
    │
    ▼
Retriever
    │
    ▼
Context Retrieval
    │
    ▼
Gemini LLM
    │
    ▼
Response
```

---

# Future Enhancements

Potential improvements:

* Docker Deployment
* Authentication & Authorization
* OWASP LLM Top 10 Security Layers

---

# Technology Stack

| Component              | Technology                 |
| ---------------------- | -------------------------- |
| API Framework          | FastAPI                    |
| Embeddings             | BAAI/bge-m3                |
| Vector Store           | FAISS                      |
| Framework              | LangChain                  |
| LLM                    | Gemini 2.5 Flash           |
| Retrieval              | MultiQueryRetriever + MMR  |
| Document Processing    | LangChain Document Loaders |
| Environment Management | python-dotenv              |

---
