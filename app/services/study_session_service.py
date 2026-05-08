from app.services.mastery_service import MasteryService, DictionaryEntry


class StudySessionService:
    def __init__(self, mastery_service: MasteryService, generator_service, vector_store):
        """
        Initializes the Orchestrator.
        Notice we don't type-hint 'generator_service' strictly, embracing duck typing!
        """
        self.mastery_service = mastery_service
        self.generator = generator_service
        self.vector_store = vector_store

    def _get_story_chunks(self, node_id: str) -> list[str]:
        """
                Uses LangChain's similarity search to find the closest story paragraphs.
                """
        # k=3 tells LangChain to return the top 3 most relevant chunks
        docs = self.vector_store.similarity_search(node_id, k=3)

        if docs:
            # LangChain returns Document objects. We just want the raw text.
            return [doc.page_content for doc in docs]

        return ["No context found in story."]


    def generate_daily_review(self, current_time: str, limit: int = 10) -> list[DictionaryEntry]:
        due_ids = self.mastery_service.get_due_nodes(current_time, limit)
        study_batch = []

        for node_id in due_ids:
            entry = self.mastery_service.get_dictionary_entry(node_id)

            if entry and entry.spanish != "":
                study_batch.append(entry)
                continue

            print(f"Cache miss for '{node_id}'. Generating flashcard...")
            chunks = self._get_story_chunks(node_id)
            new_entry = self.generator.generate_flashcard(node_id, chunks)
            self.mastery_service.save_dictionary_entry(new_entry)
            study_batch.append(new_entry)

        return study_batch