def test_ulip_4_percent():
    """
    Test Pack 9

    10 lakh investment
    at 4%.
    """

    investment = 1000000

    assert (
        investment * 1.04
        ==
        1040000
    )


def test_ulip_8_percent():
    """
    Test Pack 9

    10 lakh investment
    at 8%.
    """

    investment = 1000000

    assert (
        investment * 1.08
        ==
        1080000
    )