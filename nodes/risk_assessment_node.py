from graph.state import UnderwritingState
from utils.logger import logger


def risk_assessment_node(
    state: UnderwritingState
) -> dict:

    """
    Deterministic insurance risk assessment.

    Classifies:

    - Occupational Risk
    - Family History Risk

    No LLM usage.
    """

    logger.info(
        "--- [NODE] Risk Assessment ---"
    )

    customer_profile = state.get(
        "customer_profile",
        {}
    )

    family_profile = state.get(
        "family_profile",
        {}
    )

    # ----------------------------------
    # Long-Term Memory
    # ----------------------------------

    customer_memory = state.get(
        "customer_memory",
        []
    )

    occupation = (
        customer_profile
        .get(
            "occupation",
            ""
        )
        .lower()
    )

    family_history = (
        family_profile
        .get(
            "family_history",
            ""
        )
        .lower()
    )

    # ----------------------------------
    # Enrich Family History
    # From Mem0 Long-Term Memory
    # ----------------------------------

    memory_text = " ".join(
        customer_memory
    ).lower()

    if not family_history:

        family_history = (
            memory_text
        )

    # ----------------------------------
    # Occupational Risk
    # ----------------------------------

    occupational_risk = "STANDARD"

    if any(
        keyword in occupation
        for keyword in [
            "pilot",
            "aviation",
            "mining",
            "miner",
            "offshore",
            "drilling"
        ]
    ):
        occupational_risk = (
            "HIGH_OCCUPATIONAL_RISK"
        )

    # ----------------------------------
    # Family History Risk
    # ----------------------------------

    family_history_risk = "NONE"

    if any(
        keyword in family_history
        for keyword in [
            "bypass",
            "cardiac",
            "heart attack",
            "heart disease"
        ]
    ):
        family_history_risk = (
            "MODERATE_CARDIAC"
        )

    elif "diabetes" in family_history:

        family_history_risk = (
            "DIABETES_HISTORY"
        )

    elif "cancer" in family_history:

        family_history_risk = (
            "FAMILY_CANCER_HISTORY"
        )

    logger.info(
        f"Occupation Risk="
        f"{occupational_risk}"
    )

    logger.info(
        f"Family Risk="
        f"{family_history_risk}"
    )

    return {

        "occupational_risk":
            occupational_risk,

        "family_history_risk":
            family_history_risk,

        "visited_nodes": [
            "risk_assessment_node"
        ],

        "execution_logs": [
            (
                "Occupational risk "
                f"classified as "
                f"{occupational_risk}"
            ),
            (
                "Family history risk "
                f"classified as "
                f"{family_history_risk}"
            )
        ]
    }