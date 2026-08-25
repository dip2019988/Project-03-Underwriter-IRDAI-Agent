from typing import List, Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserLogin(BaseModel):
    username: str = Field(
        ...,
        example="advisor01"
    )

    password: str = Field(
        ...,
        example="InsurancePass123!"
    )


class UnderwritingRequest(BaseModel):

    raw_query: str = Field(
        ...,
        description="Customer insurance query",
        example=(
            "I am 34 years old, earn 18 lakh annually "
            "and want 2.5 crore term insurance. "
            "I occasionally smoke."
        )
    )

    customer_id: str = Field(
        default="CUST001"
    )


class UnderwritingResponse(BaseModel):

    thread_id: str

    customer_name: str

    customer_id: str

    intent: str

    sub_category: str

    guardrail_passed: bool

    guardrail_violation_reason: Optional[str] = None

    sanitized_query: str

    solution: str

    confidence_score: int

    risk_category: Optional[str] = None

    underwriting_recommendation: Optional[str] = None

    is_cached_response: bool

    visited_nodes: List[str]