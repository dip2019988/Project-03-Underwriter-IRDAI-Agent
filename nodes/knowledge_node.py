import re

from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


def extract_investment_amount(
    query: str
) -> float:

    query = query.lower()

    patterns = [

        # 10 lakh investment
        r'(\d+(?:\.\d+)?)\s*lakhs?\s*investment',

        # investment of 10 lakh
        r'investment\s*of\s*(\d+(?:\.\d+)?)\s*lakhs?',

        # invest 10 lakh
        r'invest(?:ing)?\s*(\d+(?:\.\d+)?)\s*lakhs?',

        # invest 2.5 crore
        r'invest(?:ing)?\s*(\d+(?:\.\d+)?)\s*crores?',

        # 10 crore investment
        r'(\d+(?:\.\d+)?)\s*crores?\s*investment',

        # investment of 2 crore
        r'investment\s*of\s*(\d+(?:\.\d+)?)\s*crores?',
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query
        )

        if match:

            value = float(
                match.group(1)
            )

            if "crore" in pattern:

                return (
                    value * 10000000
                )

            return (
                value * 100000
            )

    return 0

def knowledge_answer_node(
    state: UnderwritingState
) -> dict:

    """
    Product Information and IRDAI Knowledge Node.

    Used for:

    - PRODUCT_QUERY
    - IRDAI_COMPLIANCE

    Does NOT perform underwriting.
    Does NOT generate risk assessments.
    Does NOT generate premium decisions.
    """

    logger.info(
        "--- [NODE] Knowledge Answer Generator ---"
    )

    retrieved_docs = state.get(
        "retrieved_docs",
        []
    )

    source_references = []

    for doc in retrieved_docs:

        source_references.append(
            (
                f"{doc.get('id')} | "
                f"{doc.get('title')}"
            )
        )


    intent = state.get(
        "intent",
        "GENERAL"
    )

    sub_category = state.get(
        "sub_category",
        ""
    )

    ulip_illustration_data = {}

    ulip_illustration = ""

    query = state.get(
        "sanitized_query",
        ""
    )

    if "ULIP" in sub_category.upper():

        investment = extract_investment_amount(
            query
        )

        logger.info(
            f"[ULIP] Investment extracted: {investment}"
        )

        if investment > 0:

            scenario_4 = (
                investment * 1.04
            )

            scenario_8 = (
                investment * 1.08
            )

            logger.info(
                f"[ULIP] 4%={scenario_4}, "
                f"8%={scenario_8}"
            )

            ulip_illustration_data = {

                "investment_amount":
                    investment,

                "illustration_4_percent":
                    scenario_4,

                "illustration_8_percent":
                    scenario_8,

                "regulatory_disclosure":
                    (
                        "Illustrative only. "
                        "Market-linked returns "
                        "are not guaranteed."
                    )
            }   

            ulip_illustration = f"""
    ULIP Illustration

    Investment Amount:
    ₹{investment:,.0f}

    4% Gross Return Scenario:
    ₹{scenario_4:,.0f}

    8% Gross Return Scenario:
    ₹{scenario_8:,.0f}

    Important:
    These figures are illustrative only
    and do not represent guaranteed returns.
    Market-linked returns may vary.
    """

    system_prompt = """
You are an Insurance Knowledge Assistant.

You answer:

- IRDAI regulations
- Term insurance concepts
- ULIP concepts
- Insurance disclosures
- Life insurance product questions
- Underwriting rules and guidelines

IMPORTANT

1. Do NOT generate underwriting decisions.

2. Do NOT generate:
   - STANDARD_RATES
   - PREMIUM_LOADING_REQUIRED
   - MANDATORY_MEDICAL_TESTS
   - DECLINED

3. Do NOT generate:
   - Customer Summary
   - Financial Assessment
   - Medical Assessment
   - Lifestyle Assessment

4. Answer only the user's question.

5. Use the retrieved documents
   as the primary source.

6. If multiple documents are available,
   summarize and organize them clearly.

7. If the answer comes from IRDAI rules,
   explain the regulation in simple language.

8. If a ULIP Illustration is provided,
   you MUST display both 4% and 8%
   scenarios numerically.

9. Clearly state that market-linked
   returns are not guaranteed.

Structure:

# Answer

# Key Points

# Important Disclosure (if applicable)

"""

    context = f"""
Intent:
{intent}

Sub Category:
{sub_category}

Retrieved Documents:
{retrieved_docs}

Source References:
{source_references}

ULIP Illustration:
{ulip_illustration}

User Question:
{state.get("sanitized_query", "")}
"""

    answer = openai_service.execute_prompt(
        system_prompt=system_prompt,
        user_input=context
    )

    if source_references:

        answer += "\n\n# Sources\n\n"

        for source in source_references:

            answer += f"- {source}\n"

    logger.info(
        f"[ULIP DEBUG] Returning illustration: "
        f"{ulip_illustration_data}"
    )

    return {

        "risk_category":
            "KNOWLEDGE_QUERY",

        "ulip_illustration":
            ulip_illustration_data,

        "knowledge_response":
            answer,

        "underwriting_recommendation":
            answer,

        "solution":
            answer,

        "confidence_score":
            95,

        "visited_nodes": [
            "knowledge_answer_node"
        ],

        "execution_logs": [
            (
                "Generated knowledge answer "
                f"for {intent}"
            )
        ]
    }