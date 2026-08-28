from pydantic import BaseModel, Field

from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


class ProfileExtractionSchema(BaseModel):

    age: int = Field(default=0)

    annual_income: int = Field(default=0)

    requested_cover: int = Field(default=0)

    existing_cover: int = Field(default=0)

    smoker: bool = Field(default=False)

    height_cm: int = Field(default=0)

    weight_kg: int = Field(default=0)

    occupation: str = Field(default="")

    family_history: str = Field(default="")


def profile_extraction_node(
    state: UnderwritingState
) -> dict:

    logger.info(
        "--- [NODE] Profile Extraction ---"
    )

    system_prompt = """
You are an insurance profile extraction engine.

Extract ONLY information that is explicitly stated.

Return:

age
annual_income
requested_cover
smoker
height_cm
weight_kg
occupation
family_history
existing_cover

STRICT RULES:

1. Never guess values.

2. Never infer values.

3. Never use default assumptions.

4. If age is not mentioned:
   return 0.

5. If annual income is not mentioned:
   return 0.

6. If requested cover is not mentioned:
   return 0.

7. If existing cover is not mentioned:
   return 0.

8. If height is not mentioned:
   return 0.

9. If weight is not mentioned:
   return 0.

10. If smoking status is not mentioned:
    return false.

11. If occupation is not mentioned:
    return empty string.

12. If family history is not mentioned:
    return empty string.

13. Do not use insurance knowledge
    to estimate missing information.

EXAMPLES

Query:
What is IRDAI Section 45?

Output:
{{
  "age": 0,
  "annual_income": 0,
  "requested_cover": 0,
  "smoker": false,
  "height_cm": 0,
  "weight_kg": 0
}}

Query:
I am 34 years old and earn 18 lakh.

Output:
{{
  "age": 34,
  "annual_income": 1800000,
  "requested_cover": 0,
  "smoker": false,
  "height_cm": 0,
  "weight_kg": 0
}}

Query:
I earn 18 lakh annually, already have 50 lakh cover,
work as a commercial pilot and my father had bypass surgery.

Output:
{{
  "age": 0,
  "annual_income": 1800000,
  "requested_cover": 0,
  "existing_cover": 5000000,
  "smoker": false,
  "height_cm": 0,
  "weight_kg": 0,
  "occupation": "Commercial Pilot",
  "family_history": "Father had bypass surgery"
}}

Convert:

18 lakh -> 1800000

25 lakh -> 2500000

2.5 crore -> 25000000

Return JSON only.
"""

    extracted: ProfileExtractionSchema = (
        openai_service.execute_prompt(
            system_prompt=system_prompt,
            user_input=state.get(
                "sanitized_query",
                ""
            ),
            output_schema=ProfileExtractionSchema
        )
    )

    customer_profile = {}

    if extracted.age > 0:

        customer_profile["age"] = (
            extracted.age
        )

    if extracted.occupation:

        customer_profile[
            "occupation"
        ] = extracted.occupation

    financial_profile = {}

    if extracted.annual_income > 0:
        financial_profile[
            "annual_income"
        ] = extracted.annual_income

    if extracted.requested_cover > 0:

        financial_profile[
            "requested_cover"
        ] = extracted.requested_cover

    if extracted.existing_cover > 0:

        financial_profile[
            "existing_cover"
        ] = extracted.existing_cover

    medical_profile = {}

    if extracted.height_cm > 0:
        medical_profile[
            "height_cm"
        ] = extracted.height_cm

    if extracted.weight_kg > 0:
        medical_profile[
            "weight_kg"
        ] = extracted.weight_kg

    medical_profile[
        "smoker"
    ] = extracted.smoker

    family_profile = {}

    if extracted.family_history:

        family_profile[
            "family_history"
        ] = extracted.family_history

    logger.info(
        f"Extracted "
        f"Age={extracted.age}, "
        f"Income={extracted.annual_income}, "
        f"Cover={extracted.requested_cover}"
    )

    return {

        "customer_profile":
            customer_profile,

        "financial_profile":
            financial_profile,

        "medical_profile":
            medical_profile,

        "family_profile":
            family_profile,

        "visited_nodes": [
            "profile_extraction_node"
        ],

        "execution_logs": [
            "Customer profile extracted"
        ]
    }