def calculate_premium(
    age,
    sum_assured,
    smoker=False
):

    base_rate = 0.005

    premium = (
        sum_assured * base_rate
    )

    premium *= (1 + age / 100)

    if smoker:
        premium *= 1.25

    return round(premium, 2)
