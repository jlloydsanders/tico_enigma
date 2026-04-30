# Project State: The Tico Enigma

## 1. Architectural Overview
* **Goal:** AI-driven language learning platform (Costa Rican dialect focus).
* **Core Pattern:** Retrieval-Augmented Generation (RAG) with a Double-Streaming Audio Pipeline.
* **Infrastructure:** Dockerized Python backend, targeting Azure deployment.

## 2. Current Implementation Focus
* [ ] Write Chapter 1 (Full length for realistic data density).
* [ ] Initialize Docker environment (Python + LangChain container).
* [ ] Build initial text chunking script for data ingestion.

## 3. Naming Conventions & Glossary
* **VectorDB:** The local instance of ChromaDB/FAISS used for semantic search.
* **KnowledgeEngine:** The core LangChain orchestration module.
* **Telemetry:** The implicit/explicit data points collected for the SM-2 spaced repetition algorithm.

## 4. Pending Architectural Decisions
* Selecting the specific Text-to-Speech (TTS) API for the audio pipeline.
* Determining the schema for user progress metadata in the database.