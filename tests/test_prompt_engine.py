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
        yaml_content = """
prompts:
  greeting: Hello
  options:
    - one
    - two
"""
        expected = {"prompts": {"greeting": "Hello", "options": ["one", "two"]}}

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")

        assert result == expected

    def test_load_prompts_empty_file(self):
        """Test loading an empty YAML file returns None."""
        with patch("builtins.open", mock_open(read_data="")):
            result = load_prompts("empty.yaml")

        assert result is None

    def test_load_prompts_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            load_prompts("nonexistent.yaml")

    def test_load_prompts_invalid_yaml(self):
        """Test that invalid YAML raises a YAML error."""
        invalid_yaml = "key: [invalid: yaml: content"

        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with pytest.raises(yaml.YAMLError):
                load_prompts("invalid.yaml")

    def test_load_prompts_list_yaml(self):
        """Test loading a YAML file that contains a list at top level."""
        yaml_content = "- item1\n- item2\n- item3"
        expected = ["item1", "item2", "item3"]

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("list.yaml")

        assert result == expected

    def test_load_prompts_opens_correct_path(self):
        """Test that the function opens the file at the given path."""
        yaml_content = "key: value"

        with patch("builtins.open", mock_open(read_data=yaml_content)) as mocked_open:
            load_prompts("/some/specific/path.yaml")

        mocked_open.assert_called_once_with("/some/specific/path.yaml", "r")

    def test_load_prompts_permission_error(self):
        """Test that PermissionError propagates when file is not readable."""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                load_prompts("restricted.yaml")