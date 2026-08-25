from typing import Literal
from graph.state import UnderwritingState
from utils.logger import logger


def route_by_intent(
    state: UnderwritingState
) -> Literal[
    "kb_node",
    "mcp_node",
    "underwriting_node"
]:

    intent = state.get("intent", "GENERAL")

    logger.info(
        f"[ROUTER] Intent detected: {intent}"
    )

    if intent in [
        "HEALTH_RISK",
        "LIFESTYLE_RISK",
        "FINANCIAL_UNDERWRITING"
    ]:
        return "mcp_node"

    if intent in [
        "PRODUCT_QUERY",
        "IRDAI_COMPLIANCE"
    ]:
        return "kb_node"

    return "underwriting_node"


def evaluate_confidence_route(
    state: UnderwritingState
):

    confidence = state.get(
        "confidence_score",
        0
    )

    if confidence >= 80:
        return "END"

    if state.get(
        "retry_count",
        0
    ) < 2:
        return "solution_node"

    return "human_approval_node"