"""
Function 3 helper: base paper / reference document retrieval.
Hybrid — local RAG store first (curated/approved papers), Arxiv second.
"""
from langchain.tools import tool
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper

from rag.vectorstore import get_vectorstore

_arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=1500))


@tool
def retrieve_local_base_paper(problem_statement: str) -> str:
    """
    Searches the local base-paper store (curated PDFs already reviewed and
    approved) for a paper relevant to the given problem statement/description.
    Returns matching paper titles and file paths with similarity scores
    (lower score = closer match).
    """
    vs = get_vectorstore()
    results = vs.similarity_search_with_score(problem_statement, k=3)
    if not results:
        return "No relevant base paper found locally."

    lines = []
    for doc, score in results:
        if doc.metadata.get("type") != "base_paper":
            continue
        lines.append(
            f"title={doc.metadata.get('title')} | file_path={doc.metadata.get('file_path')} | score={score:.3f}"
        )
    return "\n".join(lines) if lines else "No relevant base paper found locally."


@tool
def search_arxiv_base_paper(query: str) -> str:
    """
    Fallback: searches Arxiv for a base paper when nothing suitable is found
    in the local store.

    Args:
        query: topic / problem statement to search Arxiv for
    """
    return _arxiv.run(query)
