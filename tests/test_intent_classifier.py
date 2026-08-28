from unittest.mock import patch

from nodes.classify_node import IntentClassificationSchema, classify_intent_node


@patch(
    "nodes.classify_node.openai_service.execute_prompt"
)
def test_ulip_intent_classification(
    mock_execute
):

    mock_execute.return_value = (
        IntentClassificationSchema(
            intent="PRODUCT_QUERY",
            sub_category="ULIPs"
        )
    )

    state = {
        "sanitized_query":
        "Explain ULIP returns"
    }

    result = (
        classify_intent_node(state)
    )

    assert (
        result["intent"]
        == "PRODUCT_QUERY"
    )

    assert (
        result["sub_category"]
        == "ULIPs"
    )