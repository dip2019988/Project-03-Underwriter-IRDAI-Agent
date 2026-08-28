import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent


def save_json(filename, data):

    with open(
        DATA_DIR / filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def generate_insurance_kb():

    kb_data = [

        # -------------------------------------------------
        # IRDAI Compliance
        # -------------------------------------------------

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
                "Policyholders have a free-look period of 15 days or 30 days for electronic and distance mode policies."
        },

        {
            "id": "IRDAI-003",
            "category": "IRDAI_COMPLIANCE",
            "title": "Anti Mis-selling Rule",
            "content":
                "Advisors must not promise guaranteed returns on market linked insurance products."
        },

        {
            "id": "IRDAI-004",
            "category": "IRDAI_COMPLIANCE",
            "title": "Mortality Charge Disclosure",
            "content":
                "Mortality charges must be disclosed separately in illustrations and policy documents."
        },

        # -------------------------------------------------
        # ULIP
        # -------------------------------------------------

        {
            "id": "ULIP-001",
            "category": "ULIP",
            "title": "ULIP Illustration Guidelines",
            "content":
                "ULIP benefit illustrations must display both 4 percent and 8 percent gross return scenarios."
        },

        {
            "id": "ULIP-002",
            "category": "ULIP",
            "title": "ULIP Structure",
            "content":
                "ULIPs combine life insurance protection with market linked investment options."
        },

        # -------------------------------------------------
        # TERM PLAN
        # -------------------------------------------------

        {
            "id": "TERM-001",
            "category": "TERM_PLAN",
            "title": "Term Insurance Overview",
            "content":
                "Term insurance provides pure life cover with no maturity benefit in most plans."
        },

        {
            "id": "TERM-002",
            "category": "TERM_PLAN",
            "title": "Smoker Classification",
            "content":
                "Any tobacco consumption during the previous twelve months is generally classified as smoker risk."
        },

        # -------------------------------------------------
        # TROP
        # -------------------------------------------------

        {
            "id": "TROP-001",
            "category": "TROP",
            "title": "Return of Premium Plan",
            "content":
                "Return of Premium plans return eligible premiums upon survival at policy maturity while providing life cover during the policy term."
        },

        # -------------------------------------------------
        # Guaranteed Income Plans
        # -------------------------------------------------

        {
            "id": "GIP-001",
            "category": "GUARANTEED_INCOME",
            "title": "Guaranteed Income Plan",
            "content":
                "Guaranteed income plans provide predefined benefits subject to policy conditions."
        },

        # -------------------------------------------------
        # HLV
        # -------------------------------------------------

        {
            "id": "HLV-001",
            "category": "HLV",
            "title": "HLV Age Multiplier Below 35",
            "content":
                "Applicants below age thirty five may qualify for up to twenty times annual income based on underwriting guidelines."
        },

        {
            "id": "HLV-002",
            "category": "HLV",
            "title": "HLV Age Multiplier 35 to 45",
            "content":
                "Applicants aged thirty five to forty five may qualify for up to fifteen times annual income."
        },

        {
            "id": "HLV-003",
            "category": "HLV",
            "title": "HLV Existing Cover Adjustment",
            "content":
                "Existing life insurance cover may be considered when determining additional financial eligibility."
        },

        # -------------------------------------------------
        # BMI
        # -------------------------------------------------

        {
            "id": "UW-001",
            "category": "UNDERWRITING_RULES",
            "title": "BMI Standard Classification",
            "content":
                "BMI may be used to determine standard, loaded, or medical underwriting decisions."
        },

        {
            "id": "UW-002",
            "category": "UNDERWRITING_RULES",
            "title": "High BMI Risk",
            "content":
                "High BMI values may lead to premium loading or additional medical requirements."
        },

        # -------------------------------------------------
        # Medical Examinations
        # -------------------------------------------------

        {
            "id": "MED-001",
            "category": "MEDICAL_RULES",
            "title": "Medical Examination Requirements",
            "content":
                "Applicants with elevated risk factors may require Tele Medical Examination, Full Medical Report, ECG, HbA1c and Lipid Profile testing."
        },

        # -------------------------------------------------
        # Family History
        # -------------------------------------------------

        {
            "id": "FAM-001",
            "category": "FAMILY_HISTORY",
            "title": "Cardiac Family History",
            "content":
                "Parental history of bypass surgery or premature cardiac disease can increase underwriting scrutiny."
        },

        {
            "id": "FAM-002",
            "category": "FAMILY_HISTORY",
            "title": "Diabetes Family History",
            "content":
                "Family history of diabetes is considered during risk assessment."
        },

        # -------------------------------------------------
        # Occupational Risk
        # -------------------------------------------------

        {
            "id": "OCC-001",
            "category": "OCCUPATIONAL_RISK",
            "title": "Mining Risk",
            "content":
                "Mining occupations are generally considered high occupational risk."
        },

        {
            "id": "OCC-002",
            "category": "OCCUPATIONAL_RISK",
            "title": "Commercial Aviation Risk",
            "content":
                "Commercial aviation professions may require additional underwriting review."
        },

        {
            "id": "OCC-003",
            "category": "OCCUPATIONAL_RISK",
            "title": "Offshore Drilling Risk",
            "content":
                "Offshore drilling occupations may attract special underwriting requirements."
        }
    ]

    save_json(
        "insurance_kb.json",
        kb_data
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
        },

        {
            "customer_id": "CUST003",
            "name": "Raj Sharma",
            "age": 42,
            "annual_income": 2500000,
            "existing_cover": 10000000,
            "dependents": 3
        },

        {
            "customer_id": "CUST004",
            "name": "Anita Patel",
            "age": 31,
            "annual_income": 1600000,
            "existing_cover": 0,
            "dependents": 2
        },

        {
            "customer_id": "CUST005",
            "name": "Vikram Singh",
            "age": 48,
            "annual_income": 3200000,
            "existing_cover": 15000000,
            "dependents": 4
        }
    ]

    save_json(
        "customer_profiles.json",
        customers
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
        },

        {
            "customer_id": "CUST003",
            "smoker": False,
            "alcohol": "Moderate",
            "family_history":
                "No significant family history",
            "bmi": 24.5
        },

        {
            "customer_id": "CUST004",
            "smoker": False,
            "alcohol": "Occasional",
            "medical_condition":
                "Asthma",
            "bmi": 26.2
        },

        {
            "customer_id": "CUST005",
            "smoker": True,
            "alcohol": "Frequent",
            "medical_condition":
                "Hypertension",
            "bmi": 31.8
        }
    ]

    save_json(
        "medical_histories.json",
        medical_data
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
        },

        {
            "customer_id": "CUST003",
            "form16_income": 2500000,
            "tax_paid": 420000,
            "pan": "LMNOP1234Q"
        }
    ]

    save_json(
        "salary_statements.json",
        salaries
    )


def generate_occupation_profiles():

    occupations = [

        {
            "customer_id": "CUST001",
            "occupation": "Software Engineer",
            "risk": "STANDARD"
        },

        {
            "customer_id": "CUST003",
            "occupation": "Commercial Pilot",
            "risk": "HIGH"
        },

        {
            "customer_id": "CUST004",
            "occupation": "Mining Engineer",
            "risk": "HIGH"
        },

        {
            "customer_id": "CUST005",
            "occupation": "Offshore Drilling Supervisor",
            "risk": "VERY_HIGH"
        }
    ]

    save_json(
        "occupation_profiles.json",
        occupations
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

    generate_occupation_profiles()

    print(
        "Insurance datasets and RAG corpus generated successfully."
    )


if __name__ == "__main__":
    main()