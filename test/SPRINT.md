SPRINT.md
Current Focus: The Engine & The Content
Goal: Connect the NumPy spaced repetition logic to the database, process the existing narrative draft, and build the invisible telemetry tracker.

Sprint 1: The Orchestrator (Data Pipeline)
Status: Pending

[ ] Create app/services/srs_engine.py and implement the pure NumPy SM-2 logic (Ensuring EF floor of 1.3).

[ ] Refactor app/services/mastery_service.py to query the updated user_progress table, pass the state vector [reps, ef, interval] to the SRSEngine, and save the computed results.

[ ] Write a single Pytest file tests/test_srs.py to assert that the NumPy math calculates the intervals correctly and respects constraints.

Sprint 2: The Content Pipeline (RAG & Chapters)
Status: Pending

[ ] Set up the LangChain RecursiveCharacterTextSplitter script.

[ ] Feed the drafted Chapters 1, 2, and 3 into the splitter.

[ ] Extract the target vocabulary (specifically highlighting the Costa Rican idioms/Tico-isms) from these chunks.

[ ] Create a seeding script to populate the SQLite knowledge_nodes / vocabulary tables with this extracted data, setting initial SM-2 states to default.

Sprint 3: The Telemetry UI (Frontend Hook)
Status: Pending

[ ] Configure FastAPI to serve a single Jinja2 HTML template.

[ ] Write a Vanilla JS script in the template that attaches event listeners to track user scroll speed and tap hesitation during progressive reading.

[ ] Create a POST endpoint in FastAPI (/api/telemetry) that receives this raw interaction data.

[ ] Write the middleware logic that converts the raw hesitation/speed metrics into the integer 0-5 quality score required by the SRSEngine.