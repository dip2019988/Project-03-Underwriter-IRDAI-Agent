from mcp_services.bmi_service import calculate_bmi


def test_standard_bmi():

    result = calculate_bmi(
        height_cm=175,
        weight_kg=70
    )

    assert result["category"] == "STANDARD"


def test_underweight_bmi():

    result = calculate_bmi(
        height_cm=175,
        weight_kg=50
    )

    assert result["category"] == "UNDERWEIGHT"


def test_overweight_bmi():

    result = calculate_bmi(
        height_cm=175,
        weight_kg=85
    )

    assert result["category"] == "OVERWEIGHT"


def test_obese_bmi():

    result = calculate_bmi(
        height_cm=175,
        weight_kg=110
    )

    assert result["category"] == "OBESE"