"""
Indexes data/resources/*.txt (notes, video descriptions, practice sets)
into a persisted Chroma store so the Resource Recommendation Agent can
semantically match topics to material.

    python -m ingestion.build_vectorstore
"""
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import RESOURCES_DIR, CHROMA_DIR

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build():
    loader = DirectoryLoader(str(RESOURCES_DIR), glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()

    # Resource files are short — index whole-file rather than chunking, so
    # each match maps back to exactly one resource (with its metadata line intact).
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    vectorstore.persist()
    print(f"Indexed {len(chunks)} resources into {CHROMA_DIR}")


if __name__ == "__main__":
    build()
