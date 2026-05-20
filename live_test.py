import os
from pathlib import Path
from dotenv import load_dotenv
from app.services.mastery_service import MasteryService
from app.services.generator_service import GeminiGeneratorService
from app.services.study_session_service import StudySessionService
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def run_live_test():
    print("🚀 Starting Proof of Life Test...")

    load_dotenv()  # <--- Add this! It reads your .env file and loads the key into memory

    # 1. Check API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY is not set in your terminal.")
        return

    # 2. Initialize the Real Services
    print("🔌 Booting services...")
    mastery = MasteryService()
    gemini = GeminiGeneratorService()

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_path = Path("data/story_vector_brain")
    vector_store = Chroma(persist_directory=str(db_path), embedding_function=embeddings)

    orchestrator = StudySessionService(mastery, gemini, vector_store)

    # 3. Force a scenario: Pick a word we KNOW isn't in the SQLite dictionary yet
    test_word = "chunche"  # A great Costa Rican word!

    print(f"🎯 Injecting '{test_word}' into the due queue...")
    # Manually tell the SRS engine this word is due right now
    mastery.update_node_mastery(test_word, 1)

    # 4. Run the Orchestrator
    from datetime import datetime, timedelta
    future_time = (datetime.now() + timedelta(days=1)).isoformat()

    print("🧠 Asking Orchestrator to generate daily review...")
    batch = orchestrator.generate_daily_review(current_time=future_time)

    # 5. Output the Results
    print(f"\n✅ Output: Returned {len(batch)} flashcards.")
    for card in batch:
        print(f"   -> [{card.node_id}] Spanish: {card.spanish} | English: {card.english}")
        print(f"      Context: {card.example_sentences[:50]}...")


if __name__ == "__main__":
    run_live_test()