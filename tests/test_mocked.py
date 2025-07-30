import pytest
from jedi_council.core import TheJediCouncil


def test_mocked_llm_response(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "Mock wisdom"
    mock_response.usage.input_tokens = 5
    mock_response.usage.output_tokens = 10
    mock_response.usage.cost = 0.0012
    mock_response.latency_ms = 150

    mocker.patch("jedi_council.core._OpenAIProvider.generate", return_value=mock_response)

    council = TheJediCouncil(model="gpt-4o")
    response = council.get_wisdom("Test message")

    assert response.text == "Mock wisdom"
    assert response.usage.input_tokens == 5
    assert response.usage.output_tokens == 10
    assert response.usage.cost == 0.0012
    assert response.latency_ms == 150
