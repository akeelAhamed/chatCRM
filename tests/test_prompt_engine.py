import pytest
from unittest.mock import patch, mock_open
import yaml

from chatbot.prompt_engine import load_prompts


class TestLoadPrompts:
    """Tests for the load_prompts function."""

    def test_load_prompts_happy_path_simple_dict(self):
        """Test loading a valid YAML file with a simple dictionary."""
        yaml_content = "greeting: Hello\nfarewell: Goodbye"
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result == {"greeting": "Hello", "farewell": "Goodbye"}

    def test_load_prompts_happy_path_nested_structure(self):
        """Test loading a valid YAML file with nested structure."""
        yaml_content = "system:\n  role: assistant\n  tone: friendly"
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result == {"system": {"role": "assistant", "tone": "friendly"}}

    def test_load_prompts_happy_path_list(self):
        """Test loading a valid YAML file containing a list."""
        yaml_content = "- prompt1\n- prompt2\n- prompt3"
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result == ["prompt1", "prompt2", "prompt3"]

    def test_load_prompts_empty_file_returns_none(self):
        """Test that an empty YAML file returns None."""
        yaml_content = ""
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result is None

    def test_load_prompts_file_not_found_raises_error(self):
        """Test that a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_prompts("/nonexistent/path/prompts.yaml")

    def test_load_prompts_invalid_yaml_raises_error(self):
        """Test that invalid YAML content raises a YAML error."""
        invalid_yaml = "key: [invalid: yaml: content"
        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with pytest.raises(yaml.YAMLError):
                load_prompts("prompts.yaml")

    def test_load_prompts_opens_file_with_correct_path(self):
        """Test that the function opens the file at the specified path."""
        yaml_content = "key: value"
        with patch("builtins.open", mock_open(read_data=yaml_content)) as mocked_file:
            load_prompts("/some/specific/path.yaml")
        mocked_file.assert_called_once_with("/some/specific/path.yaml", "r")

    def test_load_prompts_with_multiline_strings(self):
        """Test loading YAML with multiline string values."""
        yaml_content = "prompt: |\n  This is a\n  multiline prompt"
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result == {"prompt": "This is a\nmultiline prompt\n"}

    def test_load_prompts_with_special_characters(self):
        """Test loading YAML with special characters in values."""
        yaml_content = 'question: "What is 2 + 2?"'
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")
        assert result == {"question": "What is 2 + 2?"}

    def test_load_prompts_permission_error(self):
        """Test that a permission error is raised when file is not readable."""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                load_prompts("restricted.yaml")