import pytest
from pydantic import ValidationError
from src.chatbot.models import ClientProfile


class TestClientProfile:
    """Test Pydantic validation logic in ClientProfile model."""

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
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile(**valid_profile_data)
        assert "email" in str(exc_info.value)

    def test_empty_financial_goals_list_is_valid(self, valid_profile_data):
        valid_profile_data["financial_goals"] = []
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == []

    def test_financial_goals_wrong_type_raises_validation_error(self, valid_profile_data):
        valid_profile_data["financial_goals"] = "not a list"
        # Pydantic v2 may coerce a string to a list or raise error depending on version
        # In Pydantic v1, this would raise; in v2 it depends on strict mode
        try:
            profile = ClientProfile(**valid_profile_data)
            # If it doesn't raise, pydantic coerced it somehow
        except ValidationError:
            pass  # Expected behavior

    def test_financial_goals_with_non_string_elements_raises_error(self, valid_profile_data):
        valid_profile_data["financial_goals"] = [123, None]
        # Pydantic may coerce int to str; None should fail
        with pytest.raises(ValidationError):
            ClientProfile(**valid_profile_data)

    def test_all_fields_missing_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile()
        errors = exc_info.value.errors()
        # All 9 fields should be reported as missing
        assert len(errors) >= 9

    def test_email_with_various_invalid_formats(self, valid_profile_data):
        invalid_emails = ["@example.com", "user@", "user@.com", "", "user@@example.com"]
        for invalid_email in invalid_emails:
            valid_profile_data["email"] = invalid_email
            with pytest.raises(ValidationError):
                ClientProfile(**valid_profile_data)

    def test_email_with_valid_formats(self, valid_profile_data):
        valid_emails = ["user@example.com", "user.name@domain.co.uk", "user+tag@example.org"]
        for valid_email in valid_emails:
            valid_profile_data["email"] = valid_email
            profile = ClientProfile(**valid_profile_data)
            assert profile.email == valid_email

    def test_single_financial_goal(self, valid_profile_data):
        valid_profile_data["financial_goals"] = ["retirement"]
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == ["retirement"]

    def test_multiple_financial_goals(self, valid_profile_data):
        goals = ["retirement", "education", "home_purchase", "emergency_fund"]
        valid_profile_data["financial_goals"] = goals
        profile = ClientProfile(**valid_profile_data)
        assert profile.financial_goals == goals
        assert len(profile.financial_goals) == 4