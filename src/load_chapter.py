from pathlib import Path

import chromadb
from chromadb import ClientAPI
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_chapter_for_rag(file_path: Path, dialect: str, chapter_number: int,cefr_level: str) -> list[Document]:
    """
    Loads a narrative chapter, splits it into semantic chunks, and enriches
    the metadata for vector database ingestion.

    Args:
        file_path (Path): The cross-platform path to the text file.
        dialect (str): The regional dialect (e.g., 'Costa Rican').
        chapter_number (int): The sequential chapter number.
        cefr_level (str): The baseline proficiency level (e.g., 'A1').

    Returns:
        list[Document]: A list of LangChain Document objects with enriched metadata.
    """

    # Initialize the loader with the file path
    loader = TextLoader(file_path, encoding="utf-8")

    # Load the file into a list of Document objects
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    for each_text in texts:
        each_text.metadata.update({
            "CEFR": cefr_level,
            "dialect": dialect,
            "chapter": chapter_number
        })

    return texts



def start_chroma_db(file_path: Path)-> ClientAPI:
    """
       Starts a chromadb with persitant storage. Will create if file doesn't exist.

       Args:
           file_path (Path): The cross-platform path to the chromadb file.

       Returns:
           ClientAPI: chromadb client
       """
    return chromadb.PersistentClient(path=file_path)


if __name__ == "__main__":

    all_vector_documents = []

    # 1. Get the absolute path to the directory where THIS script lives
    script_dir = Path(__file__).parent.resolve()

    # 2. Navigate relative to the script directory
    # Assuming your script is in a folder (like /scripts) and /data is next to it:
    project_root = script_dir.parent
    data_dir = project_root / "data"

    for i in range(1,4):
        file_path = data_dir / f"chapter_{i}.txt"
        all_vector_documents.extend(process_chapter_for_rag(file_path=file_path, dialect="Costa Rican", chapter_number=i,
                                                    cefr_level="A1"))

    print(f"Successfully processed {len(all_vector_documents)} chunks. Starting embeddings...")

    # 1. Pivot to a free, local embedding model
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Use the absolute path strategy for the database directory
    script_dir = Path(__file__).parent.resolve()
    db_path = script_dir.parent / "data" / "tico_enigma_db"

    # 3. Ingest documents into Chroma
    vector_store = Chroma.from_documents(
        documents=all_vector_documents,
        embedding=embeddings_model,
        persist_directory=str(db_path)  # Chroma expects a string path
    )

    print(f"Database successfully built and saved to {db_path}")



