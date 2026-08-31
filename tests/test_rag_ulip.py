from nodes.knowledge_node import (
    extract_investment_amount
)


def test_ulip_10_lakh_extraction():
    """
    Test Pack 9

    Verify 10 lakh investment
    is extracted correctly.
    """

    amount = (
        extract_investment_amount(
            "Show ULIP returns "
            "illustration for "
            "10 lakh investment."
        )
    )

    assert amount == 1000000