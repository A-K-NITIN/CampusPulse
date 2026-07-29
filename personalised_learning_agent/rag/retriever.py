from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import CHROMA_DIR
from ingestion.build_vectorstore import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _get_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)


def semantic_search(query: str, k: int = 3):
    """Returns top-k (content, metadata) tuples relevant to `query`."""
    store = _get_store()
    results = store.similarity_search(query, k=k)
    return [(doc.page_content, doc.metadata) for doc in results]
