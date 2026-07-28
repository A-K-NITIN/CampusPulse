"""
RAG store for unstructured/semantic content only — base paper metadata for
function 3. Structured numeric data (attendance, marks) intentionally does
NOT go through this; see decision/checks.py and sheets/google_sheets_client.py.
"""
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import config

_embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
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
