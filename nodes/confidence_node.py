from pydantic import BaseModel, Field

from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


class ConfidenceRatingSchema(BaseModel):

    confidence_score: int = Field(
        description="Score between 0 and 100."
    )

    reasoning: str = Field(
        description="Reason for confidence score."
    )


def confidence_check_node(
    state: UnderwritingState
) -> dict:

    """
    Evaluates confidence of underwriting
    recommendation and compliance.
    """

    logger.info(
        "--- [NODE] Underwriting Confidence Assessor ---"
    )

    system_prompt = """
    You are an Insurance Quality Assurance Engine.

    Evaluate the underwriting recommendation.

    Consider:

    1. Financial underwriting completeness.
    2. Medical risk assessment completeness.
    3. Lifestyle risk evaluation.
    4. Use of retrieved regulatory documents.
    5. IRDAI compliance.
    6. Overall recommendation quality.

    Return a confidence score
    between 0 and 100.
    """

    user_input = f"""
    Customer Query:
    {state.get('raw_query', '')}

    Recommendation:
    {state.get('solution', '')}

    Retrieved Documents:
    {state.get('retrieved_docs', [])}

    BMI:
    {state.get('bmi_result', {})}

    HLV:
    {state.get('hlv_result', {})}

    Premium:
    {state.get('premium_quote', {})}
    """

    result: ConfidenceRatingSchema = (
        openai_service.execute_prompt(
            system_prompt=system_prompt,
            user_input=user_input,
            output_schema=ConfidenceRatingSchema
        )
    )

    logger.info(
        f"Confidence: "
        f"{result.confidence_score}% "
        f"- {result.reasoning}"
    )

    return {

        "confidence_score":
            result.confidence_score,

        "visited_nodes": [
            "confidence_check_node"
        ],

        "execution_logs": [
            f"Confidence assessed: "
            f"{result.confidence_score}%"
        ]
    }