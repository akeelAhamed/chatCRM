import pytest
from unittest.mock import patch, MagicMock
import json


class TestProcessInput:
    """Tests for the process_input function."""

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_happy_path_returns_json_string(self, mock_client):
        """Test that process_input returns a properly formatted JSON string."""
        # Arrange
        mock_profile = MagicMock()
        mock_profile.json.return_value = json.dumps({"name": "John Doe", "age": 30}, indent=2)
        mock_client.chat.completions.create.return_value = mock_profile

        # Import after patching module-level dependencies
        from ui import process_input

        # Act
        result = process_input("My name is John Doe and I am 30 years old.")

        # Assert
        assert result == json.dumps({"name": "John Doe", "age": 30}, indent=2)
        mock_profile.json.assert_called_once_with(indent=2)

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_calls_openai_with_correct_parameters(self, mock_client):
        """Test that the OpenAI client is called with the correct model, messages, and response_model."""
        mock_profile = MagicMock()
        mock_profile.json.return_value = "{}"
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input, ClientProfile

        user_input = "I am a new client."
        process_input(user_input)

        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial advisor assistant."},
                {"role": "user", "content": user_input}
            ],
            response_model=ClientProfile
        )

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_empty_user_input(self, mock_client):
        """Test that process_input handles empty string input."""
        mock_profile = MagicMock()
        mock_profile.json.return_value = json.dumps({}, indent=2)
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        result = process_input("")

        # Should still call the API with empty content
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == ""
        assert result == json.dumps({}, indent=2)

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_api_error_propagates(self, mock_client):
        """Test that exceptions from the OpenAI client propagate correctly."""
        mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")

        from ui import process_input

        with pytest.raises(Exception, match="API rate limit exceeded"):
            process_input("Some input")

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_long_user_input(self, mock_client):
        """Test that process_input handles very long input strings."""
        mock_profile = MagicMock()
        mock_profile.json.return_value = json.dumps({"name": "Test"}, indent=2)
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        long_input = "A" * 10000
        result = process_input(long_input)

        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == long_input
        assert result == json.dumps({"name": "Test"}, indent=2)

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_special_characters_in_input(self, mock_client):
        """Test that process_input handles special characters in user input."""
        mock_profile = MagicMock()
        mock_profile.json.return_value = json.dumps({"name": "O'Brien"}, indent=2)
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        special_input = "My name is O'Brien & I have $1,000,000 in assets <tag>"
        result = process_input(special_input)

        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == special_input
        assert "O'Brien" in result

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_json_serialization_error(self, mock_client):
        """Test behavior when the response model's json() method raises an error."""
        mock_profile = MagicMock()
        mock_profile.json.side_effect = TypeError("Object not serializable")
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        with pytest.raises(TypeError, match="Object not serializable"):
            process_input("Some input")