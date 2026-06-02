import pytest
from pydantic import ValidationError
from src.chatbot.models import ClientProfile


class TestClientProfileValidation:
    """Test Pydantic model validation logic for ClientProfile."""

    @pytest.fixture
    def valid_profile_data(self):
        return {
            "name": "John Doe",
            "date_of_birth": "1990-01-15",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "preferred_communication": "email",
            "financial_goals": ["retirement", "savings"],
            "risk_tolerance": "moderate",
            "income_range": "50000-100000",
            "assets_range": "100000-500000",
        }

    def test_valid_profile_creation(self, valid_profile_data):
        profile = ClientProfile(**valid_profile_data)
        assert profile.name == "John Doe"
        assert profile.date_of_birth == "1990-01-15"
        assert profile.email == "john.doe@example.com"
        assert profile.phone_number == "+1234567890"
        assert profile.preferred_communication == "email"
        assert profile.financial_goals == ["retirement", "savings"]
        assert profile.risk_tolerance == "moderate"
        assert profile.income_range == "50000-100000"
        assert profile.assets_range == "100000-500000"

    def test_invalid_email_raises_validation_error(self, valid_profile_data):
        valid_profile_data["email"] = "not-an-email"
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile(**valid_profile_data)
        assert "email" in str(exc_info.value)

    def test_missing_required_field_raises_validation_error(self, valid_profile_data):
        del valid_profile_data["name"]
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile(**valid_profile_data)
        assert "name" in str(exc_info.value)

    def test_missing_email_raises_validation_error(self, valid_profile_data):
        del valid_profile_data["email"]
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_empty_financial_goals_list_is_valid(self, valid_profile_data):
        valid_profile_data["financial_goals"] = []
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == []

    def test_financial_goals_must_be_list(self, valid_profile_data):
        valid_profile_data["financial_goals"] = "not a list"
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_financial_goals_items_must_be_strings(self, valid_profile_data):
        valid_profile_data["financial_goals"] = [123, 456]
        # Pydantic will coerce integers to strings
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == ["123", "456"]

    def test_email_without_domain_raises_validation_error(self, valid_profile_data):
        valid_profile_data["email"] = "john@"
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_email_without_at_sign_raises_validation_error(self, valid_profile_data):
        valid_profile_data["email"] = "johndoe.com"
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_all_fields_missing_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile()
        errors = exc_info.value.errors()
        # All 9 fields should be reported as missing
        assert len(errors) == 9

    def test_none_for_required_string_field_raises_validation_error(self, valid_profile_data):
        valid_profile_data["name"] = None
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_none_for_financial_goals_raises_validation_error(self, valid_profile_data):
        valid_profile_data["financial_goals"] = None
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_extra_fields_behavior(self, valid_profile_data):
        valid_profile_data["extra_field"] = "unexpected"
        # Default Pydantic behavior: extra fields are ignored (or allowed depending on config)
        profile = ClientProfile(**valid_profile_data)
        assert profile.name == "John Doe"

    def test_single_financial_goal(self, valid_profile_data):
        valid_profile_data["financial_goals"] = ["retirement"]
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == ["retirement"]

    def test_valid_email_variations(self, valid_profile_data):
        valid_emails = [
            "user@domain.com",
            "user.name@domain.com",
            "user+tag@domain.co.uk",
        ]
        for email in valid_emails:
            valid_profile_data["email"] = email
            profile = ClientProfile(**valid_profile_data)
            assert profile.email == email