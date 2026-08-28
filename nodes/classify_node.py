from pydantic import BaseModel, Field

from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


class IntentClassificationSchema(BaseModel):

    intent: str = Field(
        description="""
        Category:
        PRODUCT_QUERY,
        IRDAI_COMPLIANCE,
        HEALTH_RISK,
        LIFESTYLE_RISK,
        FINANCIAL_UNDERWRITING,
        GENERAL
        """
    )

    sub_category: str = Field(
        description="""
        Specific insurance sub-category.
        Examples:
        ULIP,
        TERM_PLAN,
        HLV,
        SMOKER,
        BMI,
        FAMILY_HISTORY,
        MEDICAL_TESTS
        """
    )

    contains_ulip_request: bool = Field(
        default=False,
        description="""
        True if the user requests:


        - ULIP Illustration
        - ULIP Return Projection
        - ULIP Returns
        - 4% Illustration
        - 8% Illustration
        """

    )

def classify_intent_node(
    state: UnderwritingState
) -> dict:

    logger.info(
        "--- [NODE] Insurance Intent Classification ---"
    )

    system_prompt = """
    You are an Insurance Pre-Underwriting Classifier.

    Classify the PRIMARY intent into exactly one category.

    PRODUCT_QUERY
    - Product information
    - Term plans
    - ULIPs
    - Savings plans

    IRDAI_COMPLIANCE
    - Regulatory questions
    - Disclosures
    - Free-look period
    - Section 45

    HEALTH_RISK
    - Medical condition
    - Disease
    - Surgery
    - BMI

    LIFESTYLE_RISK
    - Smoking
    - Tobacco
    - Alcohol
    - Adventure sports

    FINANCIAL_UNDERWRITING
    - Income
    - HLV
    - Sum Assured
    - Financial eligibility

    GENERAL
    - Any other insurance question

    Also provide:

    1. sub_category

    2. contains_ulip_request

    contains_ulip_request must be TRUE when the user requests:

    - ULIP illustration
    - ULIP returns
    - ULIP projection
    - ULIP growth example
    - ULIP 4% illustration
    - ULIP 8% illustration

    IMPORTANT:

    A request may contain both:

    - financial underwriting
    and
    - ULIP illustration

    In such cases:

    intent = FINANCIAL_UNDERWRITING

    contains_ulip_request = true
    """

    response: IntentClassificationSchema = (
        openai_service.execute_prompt(
            system_prompt=system_prompt,
            user_input=state["sanitized_query"],
            output_schema=IntentClassificationSchema
        )
    )

    logger.info(
        f"Intent={response.intent}, "
        f"SubCategory={response.sub_category}, "
        f"ULIP={response.contains_ulip_request}"
    )

    return {
        "intent": response.intent,
        "sub_category": response.sub_category,
        "contains_ulip_request":
            response.contains_ulip_request,
        "visited_nodes": [
            "classify_intent_node"
        ],
        "execution_logs": [
            f"Intent classified as {response.intent}"
        ]
    }