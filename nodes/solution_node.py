from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


def generate_solution_node(
    state: UnderwritingState
) -> dict:

    """
    Generates final underwriting recommendation.
    """

    logger.info(
        "--- [NODE] Underwriting Recommendation Generator ---"
    )

    memory_context = state.get(
        "customer_memory",
        {}
    )

    retrieved_docs = state.get(
        "retrieved_docs",
        []
    )

    bmi_result = state.get(
        "bmi_result",
        {}
    )

    hlv_result = state.get(
        "hlv_result",
        {}
    )

    premium_quote = state.get(
        "premium_quote",
        {}
    )

    system_prompt = """
    You are an IRDAI-compliant Life Insurance
    Underwriting Advisor.

    Your responsibilities:

    1. Review customer financial profile.
    2. Review medical profile.
    3. Review lifestyle disclosures.
    4. Use HLV calculation results.
    5. Use BMI results.
    6. Use retrieved underwriting documents.
    7. Generate an underwriting recommendation.

    IMPORTANT:

    Never promise guaranteed returns.

    Never suggest hiding medical history.

    Never suggest hiding smoking habits.

    Include mandatory insurance disclosures.

    Return professional underwriting guidance.

    Decision values MUST be one of:

    STANDARD_RATES
    PREMIUM_LOADING_REQUIRED
    MANDATORY_MEDICAL_TESTS
    DECLINED
    """

    context = f"""
    Customer Profile:
    {state.get("customer_profile", {})}

    Financial Profile:
    {state.get("financial_profile", {})}

    Medical Profile:
    {state.get("medical_profile", {})}

    Family Profile:
    {state.get("family_profile", {})}

    Long-Term Memory:
    {memory_context}

    BMI Result:
    {bmi_result}

    HLV Result:
    {hlv_result}

    Premium Quote:
    {premium_quote}

    Retrieved Documents:
    {retrieved_docs}

    User Query:
    {state.get("raw_query", "")}
    """

    recommendation = openai_service.execute_prompt(
        system_prompt=system_prompt,
        user_input=context
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    if (
        "generate_solution_node"
        in state.get(
            "visited_nodes",
            []
        )
    ):
        retry_count += 1

    return {

        "underwriting_recommendation":
        recommendation,

        "solution":
        recommendation,

        "retry_count":
        retry_count,

        "visited_nodes": [
            "generate_solution_node"
        ],

        "execution_logs": [
            "Generated insurance underwriting recommendation"
        ]
    }