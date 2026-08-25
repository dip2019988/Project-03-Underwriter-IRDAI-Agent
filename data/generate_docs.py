import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent


def generate_insurance_kb():

    kb_data = [

        {
            "id": "IRDAI-001",
            "category": "IRDAI_COMPLIANCE",
            "title": "Section 45 Incontestability Rule",
            "content":
                "Life insurance policies cannot normally be questioned after three years except in cases of fraud."
        },

        {
            "id": "IRDAI-002",
            "category": "IRDAI_COMPLIANCE",
            "title": "Free Look Period",
            "content":
                "Policyholders have a free-look period of 15 days or 30 days for electronic and distance-mode policies."
        },

        {
            "id": "ULIP-001",
            "category": "ULIP",
            "title": "ULIP Illustration Guidelines",
            "content":
                "ULIP benefit illustrations must show both 4 percent and 8 percent gross return scenarios."
        },

        {
            "id": "TERM-001",
            "category": "TERM_PLAN",
            "title": "Smoker Classification",
            "content":
                "Any tobacco consumption within the previous 12 months is generally treated as smoker classification."
        },

        {
            "id": "HLV-001",
            "category": "HLV",
            "title": "Human Life Value Calculation",
            "content":
                "Applicants below age 35 may qualify for up to 20 times annual income subject to underwriting limits."
        },

        {
            "id": "UW-001",
            "category": "UNDERWRITING_RULES",
            "title": "BMI Risk Assessment",
            "content":
                "BMI may be used to determine additional medical loading or standard underwriting classification."
        }
    ]

    with open(
        DATA_DIR / "insurance_kb.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            kb_data,
            f,
            indent=2
        )


def generate_customer_profiles():

    customers = [

        {
            "customer_id": "CUST001",
            "name": "John Smith",
            "age": 34,
            "annual_income": 1800000,
            "existing_cover": 5000000,
            "dependents": 2
        },

        {
            "customer_id": "CUST002",
            "name": "Jane Doe",
            "age": 29,
            "annual_income": 1200000,
            "existing_cover": 2000000,
            "dependents": 1
        }
    ]

    with open(
        DATA_DIR / "customer_profiles.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            customers,
            f,
            indent=2
        )


def generate_medical_histories():

    medical_data = [

        {
            "customer_id": "CUST001",
            "smoker": True,
            "alcohol": "Occasional",
            "family_history":
                "Father underwent bypass surgery at age 52",
            "bmi": 27.1
        },

        {
            "customer_id": "CUST002",
            "smoker": False,
            "alcohol": "None",
            "family_history":
                "Parental diabetes history",
            "bmi": 22.4
        }
    ]

    with open(
        DATA_DIR / "medical_histories.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            medical_data,
            f,
            indent=2
        )


def generate_salary_statements():

    salaries = [

        {
            "customer_id": "CUST001",
            "form16_income": 1800000,
            "tax_paid": 265000,
            "pan": "ABCDE1234F"
        },

        {
            "customer_id": "CUST002",
            "form16_income": 1200000,
            "tax_paid": 145000,
            "pan": "FGHIJ5678K"
        }
    ]

    with open(
        DATA_DIR / "salary_statements.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            salaries,
            f,
            indent=2
        )


def main():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    generate_insurance_kb()

    generate_customer_profiles()

    generate_medical_histories()

    generate_salary_statements()

    print(
        "Insurance underwriting datasets generated."
    )


if __name__ == "__main__":
    main()