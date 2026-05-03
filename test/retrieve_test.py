from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Initiate model
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Use the absolute path strategy for the database directory
script_dir = Path(__file__).parent.resolve()
db_path = script_dir.parent / "data" / "tico_enigma_db"

# 4. Open vector into Chroma
vector_store = Chroma(persist_directory=str(db_path),
                    embedding_function=embeddings_model
                )

# 5. Query vector store
results = vector_store.similarity_search(query="What happened at the volcano?", k=2)

for result in results:
    print(f"Content: {result.page_content}")
    print(f"Metadata: {result.metadata}")