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

        # Act
        from ui import process_input
        result = process_input("My name is John Doe and I am 30 years old.")

        # Assert
        assert result == json.dumps({"name": "John Doe", "age": 30}, indent=2)
        parsed = json.loads(result)
        assert parsed["name"] == "John Doe"
        assert parsed["age"] == 30

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_calls_openai_with_correct_parameters(self, mock_client):
        """Test that the OpenAI client is called with the correct model, messages, and response_model."""
        # Arrange
        mock_profile = MagicMock()
        mock_profile.json.return_value = "{}"
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input, ClientProfile

        user_input = "I am a new client."

        # Act
        process_input(user_input)

        # Assert
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
    def test_empty_input_still_calls_api(self, mock_client):
        """Test that empty string input is still passed to the API."""
        # Arrange
        mock_profile = MagicMock()
        mock_profile.json.return_value = "{}"
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        # Act
        result = process_input("")

        # Assert
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == ""

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_api_error_propagates(self, mock_client):
        """Test that exceptions from the OpenAI client propagate to the caller."""
        # Arrange
        mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")

        from ui import process_input

        # Act & Assert
        with pytest.raises(Exception, match="API rate limit exceeded"):
            process_input("Some input")

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_json_indent_formatting(self, mock_client):
        """Test that the response is formatted with indent=2."""
        # Arrange
        mock_profile = MagicMock()
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        # Act
        process_input("Test input")

        # Assert
        mock_profile.json.assert_called_once_with(indent=2)

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_long_input_is_passed_correctly(self, mock_client):
        """Test that very long user input is passed without truncation."""
        # Arrange
        mock_profile = MagicMock()
        mock_profile.json.return_value = "{}"
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        long_input = "A" * 10000

        # Act
        process_input(long_input)

        # Assert
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == long_input
        assert len(call_args[1]["messages"][1]["content"]) == 10000

    @patch("ui.client")
    @patch("ui.system_prompt", "You are a financial advisor assistant.")
    def test_special_characters_in_input(self, mock_client):
        """Test that special characters in user input are handled correctly."""
        # Arrange
        mock_profile = MagicMock()
        mock_profile.json.return_value = '{"name": "O\'Brien & Co."}'
        mock_client.chat.completions.create.return_value = mock_profile

        from ui import process_input

        special_input = "My name is O'Brien & Co. <script>alert('xss')</script>"

        # Act
        result = process_input(special_input)

        # Assert
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["messages"][1]["content"] == special_input
        assert result == '{"name": "O\'Brien & Co."}'