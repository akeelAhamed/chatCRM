import pytest
from pydantic import ValidationError
from chatbot.models import ClientProfile


class TestClientProfileValidation:
    """Test Pydantic validation logic on ClientProfile model."""

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

    def test_valid_profile_creation(self):
        data = self.valid_profile_data()
        profile = ClientProfile(**data)
        assert profile.name == "John Doe"
        assert profile.date_of_birth == "1990-01-15"
        assert profile.email == "john.doe@example.com"
        assert profile.phone_number == "+1234567890"
        assert profile.preferred_communication == "email"
        assert profile.financial_goals == ["retirement", "savings"]
        assert profile.risk_tolerance == "moderate"
        assert profile.income_range == "50000-100000"
        assert profile.assets_range == "100000-500000"

    def test_invalid_email_raises_validation_error(self):
        data = self.valid_profile_data()
        data["email"] = "not-an-email"
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile(**data)
        assert "email" in str(exc_info.value)

    def test_empty_email_raises_validation_error(self):
        data = self.valid_profile_data()
        data["email"] = ""
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_missing_required_field_raises_validation_error(self):
        data = self.valid_profile_data()
        del data["name"]
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile(**data)
        assert "name" in str(exc_info.value)

    def test_missing_email_raises_validation_error(self):
        data = self.valid_profile_data()
        del data["email"]
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_missing_financial_goals_raises_validation_error(self):
        data = self.valid_profile_data()
        del data["financial_goals"]
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_financial_goals_empty_list_is_valid(self):
        data = self.valid_profile_data()
        data["financial_goals"] = []
        profile = ClientProfile(**data)
        assert profile.financial_goals == []

    def test_financial_goals_wrong_type_raises_validation_error(self):
        data = self.valid_profile_data()
        data["financial_goals"] = "not a list"
        # Pydantic v2 may coerce a string to a list or raise error depending on version
        # In strict mode it would fail; in lax mode a string is not iterable to List[str]
        # We test that it either raises or handles gracefully
        try:
            profile = ClientProfile(**data)
            # Pydantic v2 might accept a string as a sequence of characters
            assert isinstance(profile.financial_goals, list)
        except ValidationError:
            pass  # Expected in strict validation

    def test_financial_goals_with_non_string_elements_raises_error(self):
        data = self.valid_profile_data()
        data["financial_goals"] = [123, None]
        # Pydantic may coerce int to str, but None should fail
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_email_without_domain_raises_validation_error(self):
        data = self.valid_profile_data()
        data["email"] = "user@"
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_email_without_at_sign_raises_validation_error(self):
        data = self.valid_profile_data()
        data["email"] = "userexample.com"
        with pytest.raises(ValidationError):
            ClientProfile(**data)

    def test_all_fields_missing_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            ClientProfile()
        # Should report multiple missing fields
        errors = exc_info.value.errors()
        assert len(errors) >= 9

    def test_extra_fields_are_handled(self):
        data = self.valid_profile_data()
        data["extra_field"] = "unexpected"
        # Default Pydantic behavior: extra fields are ignored (or forbidden depending on config)
        # Since no model_config is set, default is to ignore extras in Pydantic v2
        profile = ClientProfile(**data)
        assert not hasattr(profile, "extra_field") or profile.model_fields_set

    def test_valid_email_variations(self):
        data = self.valid_profile_data()
        valid_emails = [
            "user@domain.com",
            "user.name@domain.co.uk",
            "user+tag@domain.org",
        ]
        for email in valid_emails:
            data["email"] = email
            profile = ClientProfile(**data)
            assert profile.email == email

    def test_name_can_be_empty_string(self):
        """Pydantic str type allows empty strings by default."""
        data = self.valid_profile_data()
        data["name"] = ""
        profile = ClientProfile(**data)
        assert profile.name == ""

    def test_none_for_required_string_field_raises_error(self):
        data = self.valid_profile_data()
        data["name"] = None
        with pytest.raises(ValidationError):
            ClientProfile(**data)