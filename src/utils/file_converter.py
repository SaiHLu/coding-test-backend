import os
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader


def file_to_documents(path: str, filename: str) -> list[Document]:
    """Convert supported files into LangChain Documents."""
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return [Document(page_content=text, metadata={"source": filename})]

    elif ext == ".pdf":
        loader = PyPDFLoader(path)
        return loader.load()

    elif ext == ".docx":
        loader = Docx2txtLoader(path)
        return loader.load()

    else:
        raise ValueError(f"Unsupported file extension: {ext}")
