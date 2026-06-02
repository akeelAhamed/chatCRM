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
        yaml_content = "prompts:\n  greeting: Hello\n  farewell: Goodbye"
        expected = {"prompts": {"greeting": "Hello", "farewell": "Goodbye"}}

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

    def test_load_prompts_empty_file(self):
        """Test loading an empty YAML file returns None."""
        yaml_content = ""

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("prompts.yaml")

        assert result is None

    def test_load_prompts_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_prompts("nonexistent_file.yaml")

    def test_load_prompts_invalid_yaml(self):
        """Test that a YAML parsing error is raised for invalid YAML."""
        invalid_yaml = "key: [invalid: yaml: content"

        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with pytest.raises(yaml.YAMLError):
                load_prompts("bad.yaml")

    def test_load_prompts_opens_correct_path(self):
        """Test that the function opens the file at the given path."""
        yaml_content = "key: value"

        with patch("builtins.open", mock_open(read_data=yaml_content)) as mocked_open:
            load_prompts("/some/specific/path.yaml")

        mocked_open.assert_called_once_with("/some/specific/path.yaml", "r")

    def test_load_prompts_complex_structure(self):
        """Test loading a complex YAML structure with mixed types."""
        yaml_content = (
            "system:\n"
            "  role: assistant\n"
            "  temperature: 0.7\n"
            "  max_tokens: 150\n"
            "  stop_sequences:\n"
            "    - '\\n'\n"
            "    - 'END'\n"
        )

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = load_prompts("complex.yaml")

        assert result["system"]["role"] == "assistant"
        assert result["system"]["temperature"] == 0.7
        assert result["system"]["max_tokens"] == 150
        assert isinstance(result["system"]["stop_sequences"], list)