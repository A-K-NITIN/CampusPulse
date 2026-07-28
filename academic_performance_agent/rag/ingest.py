"""
Standalone ingestion script.
Run this whenever data/documents/base_papers/metadata.csv (or other RAG
source data) changes:

    python -m rag.ingest
"""
# Must be set BEFORE chromadb is imported (it reads this at import time)
import os
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from rag.vectorstore import build_vectorstore

if __name__ == "__main__":
    build_vectorstore()
    print("Vectorstore built/refreshed successfully.")
