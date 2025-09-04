from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
chroma = Chroma(
    embedding_function=embeddings,
    persist_directory="./.chroma_db",
    collection_name="coding-test",
)

retriever = chroma.as_retriever(search_kwargs={"k": 3})


def ingestions(documents: list[Document]):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        docs_list = text_splitter.split_documents(documents)
        chroma.add_documents(docs_list)
    except Exception as e:
        raise Exception(f"Ingestion failed: {str(e)}")


if __name__ == "__main__":
    response = retriever.invoke(input="Who is Sai Hlaing Lu?")
    print(f"Response: {response}")
