def calculate_hlv(
    annual_income,
    age,
    existing_cover
):

    if age < 35:
        multiplier = 20

    elif age < 45:
        multiplier = 15

    else:
        multiplier = 10

    max_cover = (
        annual_income * multiplier
    ) - existing_cover

    return {
        "multiplier": multiplier,
        "maximum_eligible_hlv": max_cover
    }