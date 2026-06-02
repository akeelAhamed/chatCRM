import pytest
from src.chatbot.portkey_client import get_response


class TestGetResponse:
    def test_happy_path_returns_expected_message(self):
        result = get_response("Hello")
        assert result == {'message': 'Simulated response for: Hello'}

    def test_returns_dict_with_message_key(self):
        result = get_response("test input")
        assert 'message' in result

    def test_response_contains_user_input(self):
        user_input = "What is the weather?"
        result = get_response(user_input)
        assert user_input in result['message']

    def test_empty_string_input(self):
        result = get_response("")
        assert result == {'message': 'Simulated response for: '}

    def test_special_characters_in_input(self):
        user_input = "Hello! @#$%^&*() 你好"
        result = get_response(user_input)
        assert result == {'message': 'Simulated response for: ' + user_input}

    def test_long_input_string(self):
        user_input = "a" * 10000
        result = get_response(user_input)
        assert result['message'] == 'Simulated response for: ' + user_input

    def test_whitespace_only_input(self):
        result = get_response("   ")
        assert result == {'message': 'Simulated response for:    '}

    def test_newline_in_input(self):
        user_input = "line1\nline2"
        result = get_response(user_input)
        assert result == {'message': 'Simulated response for: ' + user_input}

    def test_return_type_is_dict(self):
        result = get_response("test")
        assert isinstance(result, dict)