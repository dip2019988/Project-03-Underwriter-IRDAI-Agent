from unittest.mock import patch

from nodes.classify_node import (
    classify_intent_node
)

from graph.state import (
    UnderwritingState
)


def test_mixed_intent_detection():
    """
    Test Pack 10

    Verify that underwriting
    plus ULIP requests are
    correctly identified.
    """

    state: UnderwritingState = {
        "sanitized_query": (
            "I am 42 years old. "
            "Income 20 lakh. "
            "Need 2 crore term insurance. "
            "Show ULIP returns illustration "
            "for 10 lakh investment."
        )
    }

    with patch(
        "nodes.classify_node.openai_service.execute_prompt"
    ) as mock_llm:

        mock_llm.return_value.intent = (
            "FINANCIAL_UNDERWRITING"
        )

        mock_llm.return_value.sub_category = (
            "HLV"
        )

        mock_llm.return_value.contains_ulip_request = (
            True
        )

        result = (
            classify_intent_node(
                state
            )
        )

        assert (
            result["intent"]
            ==
            "FINANCIAL_UNDERWRITING"
        )

        assert (
            result[
                "contains_ulip_request"
            ]
            is True
        )