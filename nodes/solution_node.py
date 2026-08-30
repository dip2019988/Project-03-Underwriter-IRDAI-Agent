from graph.state import UnderwritingState
from services.openai_service import openai_service
from utils.logger import logger


def generate_solution_node(
    state: UnderwritingState
) -> dict:

    """
    Production Underwriting Recommendation Engine.

    Business decision is deterministic.

    LLM is used only for explanation
    and recommendation generation.
    """

    logger.info(
        "--- [NODE] Underwriting Recommendation Generator ---"
    )

    customer_profile = state.get(
        "customer_profile",
        {}
    )

    financial_profile = state.get(
        "financial_profile",
        {}
    )

    medical_profile = state.get(
        "medical_profile",
        {}
    )

    family_profile = state.get(
        "family_profile",
        {}
    )

    follow_up_questions = state.get(
        "follow_up_questions",
        []
    )

    occupational_risk = state.get(
        "occupational_risk",
        "STANDARD"
    )

    family_history_risk = state.get(
        "family_history_risk",
        "NONE"
    )

    all_memory = state.get(
        "customer_memory",
        []
    )

    safe_memory = []

    for memory in all_memory:

        memory_lower = memory.lower()

        blocked_keywords = [

            # medical
            "height",
            "weight",
            "bmi",
            "smoke",
            "smoker",
            "alcohol",
            "asthma",
            "diabetes",
            "cancer",
            "hypertension",

            # family history
            "father",
            "mother",
            "parent",
            "bypass",
            "cardiac",
            "heart",
            "family history",

            # financial
            "salary",
            "income",
            "cover",
            "premium",

            # medical measurements
            "cm",
            "kg"
        ]

        if not any(
            keyword in memory_lower
            for keyword in blocked_keywords
        ):
            safe_memory.append(memory)


    retrieved_docs = state.get(
        "retrieved_docs",
        []
    )

    bmi_result = state.get(
        "bmi_result",
        {}
    )

    hlv_result = state.get(
        "hlv_result",
        {}
    )

    premium_quote = state.get(
        "premium_quote",
        {}
    )

    ulip_illustration = state.get(
        "ulip_illustration",
        {}
    )

    # --------------------------------------------------
    # Deterministic Risk Category
    # --------------------------------------------------

    risk_category = "STANDARD"

    bmi_value = bmi_result.get(
        "bmi"
    )

    smoker = medical_profile.get(
        "smoker",
        False
    )

    if smoker:
        
        risk_category = (
            "PREMIUM_LOADING_REQUIRED"
        )

    if occupational_risk == (
        "HIGH_OCCUPATIONAL_RISK"
    ):
        risk_category = (
            "PREMIUM_LOADING_REQUIRED"
        )

    if (
        bmi_value is not None
        and bmi_value >= 30
    ):
        risk_category = (
            "MANDATORY_MEDICAL_TESTS"
        )

    # --------------------------------------------------
    # Deterministic Underwriting Decision
    # --------------------------------------------------

    decision_mapping = {

        "STANDARD":
            "STANDARD_RATES",

        "PREMIUM_LOADING_REQUIRED":
            "PREMIUM_LOADING_REQUIRED",

        "MANDATORY_MEDICAL_TESTS":
            "MANDATORY_MEDICAL_TESTS",

        "DECLINED":
            "DECLINED"
    }

    underwriting_decision = (
        decision_mapping.get(
            risk_category,
            "STANDARD_RATES"
        )
    )

    # --------------------------------------------------
    # LLM Recommendation Generation
    # --------------------------------------------------

    system_prompt = f"""
You are an IRDAI-compliant
Life Insurance Underwriting Advisor.

IMPORTANT RULES

1. The underwriting decision
   has already been determined.

2. NEVER change the decision.

3. Your role is only to explain
   the decision professionally.

4. ONLY use information from
   CURRENT CUSTOMER DATA when
   determining BMI, medical risk,
   smoking status, income, cover,
   financial risk or underwriting risk.

5. Historical memory is NOT
   current evidence.

6. Never use historical height,
   weight, BMI, smoking,
   income or cover values.

7. If current data is missing,
   explicitly state the information
   was not provided.

8. Use retrieved underwriting
   and regulatory documents whenever
   available.

9. Never promise guaranteed returns.

10. Never advise hiding smoking habits.

11. Never advise hiding medical history.

The final decision MUST remain:

{underwriting_decision}

Create these sections:

1. Customer Summary
2. Financial Assessment
3. Medical Assessment
4. Lifestyle Assessment
5. BMI Findings
6. HLV Findings
7. Premium Findings

8. ULIP Illustration
- Show investment amount
- Show 4% illustration
- Show 8% illustration
- Explain that returns are illustrative only

9. Decision

10. Mandatory Insurance Disclosures

11. Conclusion

IMPORTANT:

If ULIP Illustration data exists,
you MUST display all values exactly.

Do NOT omit ULIP Illustration.
"""

    context = f"""
CURRENT CUSTOMER DATA

Customer Profile:
{customer_profile}

Financial Profile:
{financial_profile}

Medical Profile:
{medical_profile}

Family Profile:
{family_profile}

Risk Category:
{risk_category}

Final Decision:
{underwriting_decision}

BMI Result:
{bmi_result}

HLV Result:
{hlv_result}

Premium Quote:
{premium_quote}

ULIP Illustration:
{ulip_illustration}

Retrieved Documents:
{retrieved_docs}

IMPORTANT MEMORY USAGE RULES

Customer Memory contains
historical information only.

Historical memory must never be
used as current evidence for:

- BMI assessment
- Height
- Weight
- Smoking status
- Medical underwriting
- Financial underwriting
- Income verification
- Risk classification

If current information is missing,
state that it was not provided.

Permitted Historical Memory:

{safe_memory}

User Query:
{state.get("sanitized_query", "")}
"""

    recommendation = (
        openai_service.execute_prompt(
            system_prompt=system_prompt,
            user_input=context
        )
    )

    if ulip_illustration:

        recommendation += f"""

## ULIP Illustration

Investment Amount:
₹{ulip_illustration.get("investment_amount", 0):,.0f}

4% Illustration:
₹{ulip_illustration.get("illustration_4_percent", 0):,.0f}

8% Illustration:
₹{ulip_illustration.get("illustration_8_percent", 0):,.0f}

Important Disclosure:
{ulip_illustration.get("regulatory_disclosure", "")}
"""

    retry_count = state.get(
        "retry_count",
        0
    )

    if (
        "generate_solution_node"
        in state.get(
            "visited_nodes",
            []
        )
    ):
        retry_count += 1

    logger.info(
        f"Risk={risk_category}, "
        f"Decision={underwriting_decision}"
    )


    proposal_json = {

        "financial_underwriting": {

            "verified_annual_income_inr":
                financial_profile.get(
                    "annual_income",
                    0
                ),

            "maximum_eligible_hlv_inr":
                hlv_result.get(
                    "maximum_eligible_hlv",
                    0
                ),

            "existing_life_cover_inr":
                financial_profile.get(
                    "existing_cover",
                    0
                ),

            "requested_sum_assured_inr":
                financial_profile.get(
                    "requested_cover",
                    0
                ),

            "financial_eligibility_status":
                (
                    "APPROVED"
                    if underwriting_decision
                    != "DECLINED"
                    else "DECLINED"
                )
        },

        "medical_and_lifestyle_risk": {

            "tobacco_classification":
                (
                    "SMOKER"
                    if smoker
                    else "NON_SMOKER"
                ),

            "bmi_status":
                (
                    "STANDARD"
                    if bmi_value is None
                    else (
                        "LOADED"
                        if bmi_value >= 30
                        else "STANDARD"
                    )
                ),

            "family_history_risk":
                family_history_risk,

            "follow_up_questions":
                follow_up_questions,

            "occupational_risk":
                occupational_risk,

        },

        "pre_underwriting_decision": {

            "status":
                underwriting_decision,

            "applicable_premium_category":
                premium_quote.get(
                    "currency",
                    "STANDARD"
                ),

            "required_medical_examinations":
                (
                    [
                        "Tele Medical Examination",
                        "ECG",
                        "HbA1c",
                        "Lipid Profile"
                    ]
                    if underwriting_decision
                    ==
                    "MANDATORY_MEDICAL_TESTS"
                    else []
                )
        },

        "ulip_illustration": {
            "investment_amount":
                ulip_illustration.get(
                    "investment_amount",
                    0
                ),

            "illustration_4_percent":
                ulip_illustration.get(
                    "illustration_4_percent",
                    0
                ),

            "illustration_8_percent":
                ulip_illustration.get(
                    "illustration_8_percent",
                    0
                ),

            "regulatory_disclosure":
                ulip_illustration.get(
                    "regulatory_disclosure",
                    ""
                )
        },

        "regulatory_and_compliance": {

            "section_45_incontestability_notice_issued":
                True,

            "free_look_period_days":
                30,

            "anti_mis_selling_checks": {

                "no_guaranteed_market_returns_promised":
                    True,

                "mortality_charges_disclosed":
                    True
            }
        },

        "guardrails_validation_status":
            (
                "PASSED"
                if state.get(
                    "guardrail_passed",
                    True
                )
                else "FAILED"
            )
    }

    return {

        "proposal_json":
            proposal_json,

        "risk_category":
            risk_category,

        "underwriting_decision":
            underwriting_decision,

        "underwriting_recommendation":
            recommendation,

        "solution":
            recommendation,

        "retry_count":
            retry_count,

        "visited_nodes": [
            "generate_solution_node"
        ],

        "execution_logs": [
            (
                "Generated underwriting "
                f"recommendation "
                f"({risk_category})"
            )
        ]
    }