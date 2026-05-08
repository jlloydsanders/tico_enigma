import os
import json
from google import genai
from google.genai import types

# Assuming you put DictionaryEntry in mastery_service or a models file.
# Adjust the import path if necessary!
from app.services.dictionary_engine import DictionaryEntry


class GeminiGeneratorService:
    def __init__(self, api_key: str = None):
        # Allow passing a key directly, otherwise look for the environment variable
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing. Please set it as an environment variable.")

        self.client = genai.Client(api_key=self.api_key)

    def generate_flashcard(self, node_id: str, context_chunks: list[str]) -> DictionaryEntry:
        """Takes a word ID and story chunks, and returns a populated DictionaryEntry."""

        # Combine the ChromaDB chunks into one readable string
        context_text = "\n\n".join(context_chunks)

        prompt = f"""
        You are an expert Costa Rican Spanish teacher. 
        I am giving you a target word/concept ID: '{node_id}' and some story context where it appears.
        Extract the exact Spanish word, provide its English translation, and select the best example sentence from the context.

        Story Context:
        {context_text}
        """

        # We force Gemini to return strict JSON matching this exact schema
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "spanish": types.Schema(type=types.Type.STRING),
                        "english": types.Schema(type=types.Type.STRING),
                        "example_sentences": types.Schema(type=types.Type.STRING),
                    },
                    required=["spanish", "english", "example_sentences"]
                )
            )
        )

        # Because of the schema above, we know this json.loads will never fail
        data = json.loads(response.text)

        return DictionaryEntry(
            node_id=node_id,
            spanish=data["spanish"],
            english=data["english"],
            example_sentences=data["example_sentences"]
        )