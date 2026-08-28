from nodes.knowledge_node import extract_investment_amount


def test_ulip_ignores_income_amount():

    query = (
        "I earn 20 lakh annually "
        "and want a ULIP illustration "
        "for 10 lakh investment"
    )

    amount = (
        extract_investment_amount(
            query
        )
    )

    assert amount == 1000000


def test_extract_10_lakh():

    assert (
        extract_investment_amount(
            "Show ULIP illustration for 10 lakh investment"
        )
        == 1000000
    )


def test_extract_18_lakhs():

    assert (
        extract_investment_amount(
            "Invest 18 lakhs"
        )
        == 1800000
    )


def test_extract_2_5_crore():

    assert (
        extract_investment_amount(
            "Invest 2.5 crore"
        )
        == 25000000
    )