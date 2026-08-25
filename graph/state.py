from __future__ import annotations

from typing import TypedDict, Dict, Any, List, Annotated
import operator


class UnderwritingState(TypedDict):

    # Applicant Information

    customer_id: str
    customer_name: str

    # Conversation

    raw_query: str
    sanitized_query: str

    # Presidio

    presidio_token_map: Dict[str, str]

    # Memory

    customer_memory: List[str]

    # Profile

    customer_profile: Dict[str, Any]
    financial_profile: Dict[str, Any]
    medical_profile: Dict[str, Any]
    family_profile: Dict[str, Any]

    # Classification

    intent: str
    sub_category: str

    # RAG

    retrieved_docs: List[Dict[str, Any]]

    # Tool Outputs

    bmi_result: Dict[str, Any]
    hlv_result: Dict[str, Any]
    premium_quote: Dict[str, Any]

    # Risk Assessment

    risk_score: int
    risk_category: str

    # Recommendation

    solution: str
    underwriting_recommendation: str


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

    visited_nodes: Annotated[List[str], operator.add]
    execution_logs: Annotated[List[str], operator.add]
