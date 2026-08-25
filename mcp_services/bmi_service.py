def calculate_bmi(height_cm, weight_kg):

    bmi = weight_kg / ((height_cm / 100) ** 2)

    if bmi < 18.5:
        category = "UNDERWEIGHT"

    elif bmi < 25:
        category = "STANDARD"

    elif bmi < 30:
        category = "OVERWEIGHT"

    else:
        category = "OBESE"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }