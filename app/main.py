import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from pathlib import Path

# Import our backend services
from app.services.mastery_service import MasteryService
from app.services.generator_service import GeminiGeneratorService
from app.services.study_session_service import StudySessionService
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel

# Load environment variables (API Key)
load_dotenv()

# Global variable to hold our Orchestrator in memory
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """This runs exactly once when the server boots up."""
    global orchestrator
    print("🔌 Booting the Tico Enigma Brain...")

    # Check for API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️ WARNING: GEMINI_API_KEY is not set. Generation will fail.")

    mastery = MasteryService()
    gemini = GeminiGeneratorService()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_path = Path("data/story_vector_brain")
    vector_store = Chroma(persist_directory=str(db_path), embedding_function=embeddings)

    orchestrator = StudySessionService(mastery, gemini, vector_store)
    print("🧠 Brain is online and ready.")

    yield  # The server runs and waits for requests here

    print("💤 Shutting down gracefully...")


# Initialize the API with the lifespan
app = FastAPI(
    title="Tico Enigma Core API",
    description="The spaced-repetition and AI generation backend for Costa Rican Spanish.",
    version="1.0.0",
    lifespan=lifespan
)


# --- DEPENDENCIES ---
def get_study_session() -> StudySessionService:
    """Dependency Injection: Hands the orchestrator to any route that needs it."""
    return orchestrator

class ReviewSubmission(BaseModel):
    """Defines the exact JSON payload the frontend must send us."""
    node_id: str
    grade: int  # e.g., 0 (Failed/Forgot), 1 (Hard), 2 (Good), 3 (Easy)

# --- ROUTES ---
@app.get("/health")
def health_check():
    return {"status": "online", "message": "Pura vida. The server is awake."}


@app.get("/daily-review")
def get_daily_review(service: StudySessionService = Depends(get_study_session)):
    """
    Fetches today's due flashcards. 
    If a word is missing its definition, it triggers Gemini to generate it in real-time.
    """
    from datetime import datetime, timedelta

    # Using tomorrow's date just to ensure we catch the 'chunche' test word we injected earlier
    future_time = (datetime.now() + timedelta(days=1)).isoformat()

    batch = service.generate_daily_review(current_time=future_time)

    # FastAPI automatically converts your dataclasses into perfect JSON!
    return {"due_cards": batch}


@app.post("/submit-review")
def submit_review(submission: ReviewSubmission, service: StudySessionService = Depends(get_study_session)):
    """
    Receives the user's grade for a flashcard and updates the SRS database.
    """
    # Drill into the orchestrator to hit the MasteryService
    service.mastery_service.update_node_mastery(submission.node_id, submission.grade)

    # Return a success confirmation
    return {
        "status": "success",
        "message": f"Successfully updated SRS math for '{submission.node_id}' with grade {submission.grade}"
    }