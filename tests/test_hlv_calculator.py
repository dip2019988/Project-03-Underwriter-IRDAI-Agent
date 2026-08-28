from mcp_services.hlv_service import calculate_hlv


def test_hlv_age_below_35():

    result = calculate_hlv(
        annual_income=1800000,
        age=34,
        existing_cover=5000000
    )

    assert result["multiplier"] == 20

    assert (
        result["maximum_eligible_hlv"]
        == 31000000
    )


def test_hlv_age_between_35_and_45():

    result = calculate_hlv(
        annual_income=1800000,
        age=40,
        existing_cover=0
    )

    assert result["multiplier"] == 15

    assert (
        result["maximum_eligible_hlv"]
        == 27000000
    )


def test_hlv_age_45_plus():

    result = calculate_hlv(
        annual_income=1800000,
        age=50,
        existing_cover=0
    )

    assert result["multiplier"] == 10

    assert (
        result["maximum_eligible_hlv"]
        == 18000000
    )