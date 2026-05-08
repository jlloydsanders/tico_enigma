import pytest
from unittest.mock import MagicMock, patch
from app.services.generator_service import GeminiGeneratorService


# We use @patch to intercept the genai.Client before it is created
@patch("app.services.generator_service.genai.Client")
def test_gemini_flashcard_generation(mock_client_class):
    # 1. Arrange: Setup the Fake API Response
    mock_response = MagicMock()
    # This simulates what Gemini would return based on our strict schema
    mock_response.text = '{"spanish": "brete", "english": "work/job", "example_sentences": "Tengo mucho brete hoy."}'

    # Wire the fake response into the mock client
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.models.generate_content.return_value = mock_response

    # Initialize our service (it will use the mocked client)
    # We pass a fake key so it doesn't throw the ValueError
    service = GeminiGeneratorService(api_key="fake_test_key")

    node_id = "brete"
    fake_chunks = [
        "El mae estaba cansado.",
        "Tengo mucho brete hoy, no puedo salir.",
        "Pura vida."
    ]

    # 2. Act
    result_entry = service.generate_flashcard(node_id, fake_chunks)

    # 3. Assert
    # Did the service correctly parse the JSON into our dataclass?
    assert result_entry.node_id == "brete"
    assert result_entry.spanish == "brete"
    assert result_entry.english == "work/job"
    assert "Tengo mucho brete hoy" in result_entry.example_sentences

    # Principal Check: Did the service actually call the API with our prompt?
    mock_client_instance.models.generate_content.assert_called_once()