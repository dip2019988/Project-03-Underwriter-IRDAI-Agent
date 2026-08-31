from graph.state import UnderwritingState

from nodes.risk_assessment_node import (
    risk_assessment_node
)


def test_memory_reuse_for_diabetes_history():
    """
    Test Pack 8

    Memory should influence
    underwriting risk assessment.
    """

    state: UnderwritingState = {

        "family_profile": {},

        "customer_memory": [

            "User's father has diabetes."
        ]
    }

    result = (
        risk_assessment_node(
            state
        )
    )

    assert (
        result[
            "family_history_risk"
        ]
        ==
        "DIABETES_HISTORY"
    )