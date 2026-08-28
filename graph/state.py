from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


class UnderwritingState(TypedDict):

    # Applicant Information

    customer_id: str
    customer_name: str

    # Conversation

    raw_query: str
    sanitized_query: str

    # Presidio

    presidio_token_map: dict[str, str]

    # Memory

    customer_memory: list[str]

    # Profile

    customer_profile: dict[str, Any]
    financial_profile: dict[str, Any]
    medical_profile: dict[str, Any]
    family_profile: dict[str, Any]

    # Classification

    intent: str
    sub_category: str
    contains_ulip_request: bool

    # RAG

    retrieved_docs: list[dict[str, Any]]

    # Tool Outputs

    bmi_result: dict[str, Any]
    hlv_result: dict[str, Any]
    premium_quote: dict[str, Any]

    ulip_illustration: dict[str, Any]

    # Risk Assessment

    risk_score: int
    risk_category: str

    occupational_risk: str
    family_history_risk: str
    follow_up_questions: list[str]

    # Recommendation

    solution: str
    underwriting_recommendation: str
    underwriting_decision: str
    proposal_json: dict[str, Any]


    # Guardrails

    guardrail_passed: bool
    guardrail_violation_reason: str

    # Confidence

    confidence_score: int

    # Human Review

    human_approved: bool
    human_feedback: str

    # Retry
    is_cached_response: bool
    retry_count: int

    # Tracing

    visited_nodes: Annotated[list[str], operator.add]
    execution_logs: Annotated[list[str], operator.add]
