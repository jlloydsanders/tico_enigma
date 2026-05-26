# PROJECT_STATE: The Tico Enigma

## 1. Architectural Overview
* **Goal:** AI-driven language learning platform (Costa Rican dialect focus).
* **Core Pattern:** Decoupled Client-Server (Streamlit UI + FastAPI Backend).
* **Data Layer:** Local ChromaDB (Semantic Search) + SQLite (Relational State).
* **Logic Layer:** Pure Python MasteryService (SM-2 Spaced Repetition).

## 2. Recent Completions (Sprints 1-4)
* [x] Initialize Docker/local environment and standard project structure.
* [x] Ingest Chapter 1-3 text into ChromaDB using `RecursiveCharacterTextSplitter`.
* [x] Build `StudySessionService` with Cache-Aside pattern for LLM generation.
* [x] Build `MasteryService` (SM-2 logic with 1.3 EF floor, mapped to 0-3 grading scale).
* [x] Deploy FastAPI orchestrator with Lifespan Dependency Injection.
* [x] Deploy Streamlit frontend and wire POST `/submit-review` to backend.

## 3. Current Implementation Focus (Sprint 5)
* [ ] **Vocabulary Extraction:** Identify target Costa Rican idioms and vocab from Chapters 1-3.
* [ ] **Database Seeding:** Populate the `knowledge_nodes` SQLite table with the target vocabulary and default SM-2 states.
* [ ] **Progressive Reading Hook:** Implement the logic that queries `user_progress` to determine which English words should be dynamically swapped to Spanish during chapter rendering.
* [ ] **Narrative Orchestration:** Define the exact `mastery_service` threshold (e.g., "5 nodes mastered") required to unlock Chapter 2.

## 4. Naming Conventions & Glossary
* **VectorDB (`story_vector_brain`):** Local ChromaDB instance holding chapter chunks.
* **RelationalDB (`memory_engine.db`):** Local SQLite DB tracking user states.
* **`user_progress` Table:** Tracks SM-2 states (`reps`, `easiness_factor`, `interval`, `next_review`).
* **Implicit/Explicit Telemetry:** Data points captured by the UI to calculate the 0-3 quality score.

## 5. Pending Architectural Decisions
* **Text-to-Speech (TTS):** Selecting the specific TTS API to implement the double-streaming audio pipeline.
* **Progressive Logic:** Deciding if the LLM dynamically translates text on-the-fly based on mastery, or if we use static regex/string-replacement for predefined nodes to save API costs.