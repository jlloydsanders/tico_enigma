from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from pathlib import Path


def process_chapter_for_rag(file_path: Path, dialect:str, chapter_number: int,cefr_level: str) -> list[Document]:
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



if __name__ == "__main__":

    all_vector_documents = []

    for i in range(1,4):
        file_path = Path("..") / "data" / f"""chapter_{i}.txt"""
        all_vector_documents.extend(process_chapter_for_rag(file_path=file_path, dialect="Costa Rican", chapter_number=i,
                                                    cefr_level="A1"))


    print(all_vector_documents)