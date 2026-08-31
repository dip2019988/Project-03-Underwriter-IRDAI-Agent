from graph.state import UnderwritingState

from nodes.risk_assessment_node import (
    risk_assessment_node
)


def test_cardiac_family_history():
    """
    Test Pack 4

    Father bypass surgery
    should become
    MODERATE_CARDIAC.
    """

    state: UnderwritingState = {

        "family_profile": {
            "family_history":
                (
                    "Father underwent "
                    "bypass surgery "
                    "at age 52"
                )
        }
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
        "MODERATE_CARDIAC"
    )


def test_diabetes_family_history():
    """
    Family diabetes history
    should become
    DIABETES_HISTORY.
    """

    state: UnderwritingState = {

        "family_profile": {
            "family_history":
                (
                    "Father has diabetes"
                )
        }
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