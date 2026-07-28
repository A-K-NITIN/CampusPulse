"""
RAG store for unstructured/semantic content only — base paper metadata for
function 3. Structured numeric data (attendance, marks) intentionally does
NOT go through this; see decision/checks.py and sheets/google_sheets_client.py.
"""
import os
# Suppress ChromaDB's noisy telemetry error (must be set before chromadb imports)
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
import httpx
import pandas as pd
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma

import config


class OpenRouterEmbeddings(Embeddings):
    """
    Calls OpenRouter's /embeddings endpoint directly via httpx, bypassing the
    openai SDK's strict response parser that raises 'No embedding data received'
    when the response format differs slightly from OpenAI's canonical schema.
    """

    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _embed(self, texts: List[str]) -> List[List[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "input": texts}
        response = httpx.post(
            f"{self.base_url}/embeddings",
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        # Handle both {"data": [{"embedding": [...]}]} and flat {"embeddings": [...]}
        if "data" in data:
            return [item["embedding"] for item in data["data"]]
        if "embeddings" in data:
            return data["embeddings"]
        raise ValueError(f"Unexpected embedding response shape: {list(data.keys())}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0]


_embeddings = OpenRouterEmbeddings(
    model=config.EMBEDDING_MODEL,
    api_key=config.OPENROUTER_API_KEY,
    base_url=config.OPENROUTER_BASE_URL,
)
_vectorstore = None


def _load_base_paper_documents() -> list:
    docs = []
    if not os.path.exists(config.BASE_PAPERS_METADATA_CSV):
        return docs
    df = pd.read_csv(config.BASE_PAPERS_METADATA_CSV)
    for _, row in df.iterrows():
        content = f"{row['title']}. Keywords: {row['keywords']}"
        docs.append(Document(
            page_content=content,
            metadata={
                "type": "base_paper",
                "paper_id": row["paper_id"],
                "title": row["title"],
                "file_path": row["file_path"],
            },
        ))
    return docs


def build_vectorstore() -> Chroma:
    """Run this once (or whenever source data changes) to (re)build the index."""
    docs = _load_base_paper_documents()
    if not docs:
        docs = [Document(page_content="No base papers indexed yet.", metadata={"type": "placeholder"})]

    vs = Chroma.from_documents(
        documents=docs,
        embedding=_embeddings,
        persist_directory=config.VECTORSTORE_DIR,
    )
    return vs


def get_vectorstore() -> Chroma:
    """Load the persisted vectorstore, building it if it doesn't exist yet."""
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    if os.path.exists(config.VECTORSTORE_DIR) and os.listdir(config.VECTORSTORE_DIR):
        _vectorstore = Chroma(
            persist_directory=config.VECTORSTORE_DIR,
            embedding_function=_embeddings,
        )
    else:
        _vectorstore = build_vectorstore()

    return _vectorstore
