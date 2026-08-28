from pydantic import BaseModel, Field

from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


class ConfidenceRatingSchema(BaseModel):

    confidence_score: int = Field(
        description="Score between 0 and 100."
    )

    reasoning: str = Field(
        description="Explanation."
    )


def confidence_check_node(
    state: UnderwritingState
) -> dict:

    """
    Hybrid confidence engine.

    Uses objective signals first,
    then lets the LLM refine.
    """

    logger.info(
        "--- [NODE] Underwriting Confidence Assessor ---"
    )

    score = 40
    reasoning = []

    # ----------------------------------
    # Structured Profile Extraction
    # ----------------------------------

    customer_profile = state.get(
        "customer_profile",
        {}
    )

    financial_profile = state.get(
        "financial_profile",
        {}
    )

    medical_profile = state.get(
        "medical_profile",
        {}
    )

    if customer_profile.get("age"):
        score += 10
        reasoning.append(
            "Age extracted"
        )

    if financial_profile.get(
        "annual_income"
    ):
        score += 10
        reasoning.append(
            "Income extracted"
        )

    if financial_profile.get(
        "requested_cover"
    ):
        score += 10
        reasoning.append(
            "Requested cover extracted"
        )

    # ----------------------------------
    # MCP Results
    # ----------------------------------

    if state.get("hlv_result"):
        score += 10
        reasoning.append(
            "HLV available"
        )

    if state.get("bmi_result"):
        score += 5
        reasoning.append(
            "BMI available"
        )

    if state.get("premium_quote"):
        score += 10
        reasoning.append(
            "Premium quote available"
        )

    # ----------------------------------
    # KB/RAG
    # ----------------------------------

    retrieved_docs = state.get(
        "retrieved_docs",
        []
    )

    if retrieved_docs:
        score += 10
        reasoning.append(
            f"{len(retrieved_docs)} KB docs retrieved"
        )

    # ----------------------------------
    # Recommendation Quality
    # ----------------------------------

    recommendation = state.get(
        "solution",
        ""
    )

    if recommendation:

        if len(recommendation) > 500:
            score += 5

        if (
            "Decision"
            in recommendation
        ):
            score += 5

    # ----------------------------------
    # Risk Category Present
    # ----------------------------------

    if state.get(
        "risk_category"
    ):
        score += 5
        reasoning.append(
            "Risk category determined"
        )

    score = min(score, 95)

    # ----------------------------------
    # Optional LLM Assessment
    # ----------------------------------

    system_prompt = """
    Review the underwriting recommendation.

    Return:

    confidence_score:
    between 0 and 100

    reasoning:
    concise explanation

    Avoid major deviations from
    the supplied base score.
    """

    user_input = f"""
Base Score:
{score}

Recommendation:
{recommendation}

Retrieved Docs:
{retrieved_docs}

HLV:
{state.get("hlv_result", {})}

BMI:
{state.get("bmi_result", {})}

Premium:
{state.get("premium_quote", {})}
"""

    try:

        llm_result: ConfidenceRatingSchema = (
            openai_service.execute_prompt(
                system_prompt=system_prompt,
                user_input=user_input,
                output_schema=ConfidenceRatingSchema
            )
        )

        final_score = int(
            (
                score * 0.8
            ) +
            (
                llm_result.confidence_score * 0.2
            )
        )

        final_score = min(
            final_score,
            95
        )

        final_reasoning = (
            f"Objective Score={score}. "
            f"{llm_result.reasoning}"
        )

    except Exception:

        final_score = score

        final_reasoning = (
            ", ".join(reasoning)
        )

    logger.info(
        f"Confidence: "
        f"{final_score}% - "
        f"{final_reasoning}"
    )

    return {

        "confidence_score":
            final_score,

        "visited_nodes": [
            "confidence_check_node"
        ],

        "execution_logs": [
            (
                "Confidence assessed: "
                f"{final_score}%"
            )
        ]
    }