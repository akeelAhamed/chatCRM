from pydantic import BaseModel, EmailStr
from typing import List

class ClientProfile(BaseModel):
    name: str
    date_of_birth: str
    email: EmailStr
    phone_number: str
    preferred_communication: str
    financial_goals: List[str]
    risk_tolerance: str
    income_range: str
    assets_range: str
