import pytest
from unittest.mock import patch, mock_open
import yaml

from chatbot.prompt_engine import load_prompts


class TestLoadPrompts:
    def test_load_prompts_happy_path(self):
        """Test loading a valid YAML file returns parsed content."""
        yaml_content = "greeting: Hello\nfarewell: Goodbye"
        expected = {"greeting": "Hello", "farewell": "Goodbye"}

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")

        assert result == expected

    def test_load_prompts_nested_yaml(self):
        """Test loading a YAML file with nested structure."""
        yaml_content = "prompts:\n  system: You are a bot\n  user: Hi"
        expected = {"prompts": {"system": "You are a bot", "user": "Hi"}}

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")

        assert result == expected

    def test_load_prompts_list_yaml(self):
        """Test loading a YAML file containing a list."""
        yaml_content = "- item1\n- item2\n- item3"
        expected = ["item1", "item2", "item3"]

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")

        assert result == expected

    def test_load_prompts_empty_file_returns_none(self):
        """Test loading an empty YAML file returns None."""
        yaml_content = ""

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("empty.yaml")

        assert result is None

    def test_load_prompts_file_not_found_raises_error(self):
        """Test that a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_prompts("nonexistent_file.yaml")

    def test_load_prompts_invalid_yaml_raises_error(self):
        """Test that invalid YAML content raises a YAML error."""
        invalid_yaml = "key: [invalid: yaml: content"

        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with pytest.raises(yaml.YAMLError):
                load_prompts("invalid.yaml")

    def test_load_prompts_opens_correct_path(self):
        """Test that the function opens the file at the given path."""
        yaml_content = "key: value"

        with patch("builtins.open", mock_open(read_data=yaml_content)) as mocked_open:
            load_prompts("/some/specific/path.yaml")

        mocked_open.assert_called_once_with("/some/specific/path.yaml", "r")

    def test_load_prompts_with_unicode_content(self):
        """Test loading YAML with unicode characters."""
        yaml_content = "greeting: こんにちは\nemoji: 🤖"
        expected = {"greeting": "こんにちは", "emoji": "🤖"}

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("unicode.yaml")

        assert result == expected

    def test_load_prompts_permission_error(self):
        """Test that a permission error is raised when file is not readable."""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                load_prompts("restricted.yaml")