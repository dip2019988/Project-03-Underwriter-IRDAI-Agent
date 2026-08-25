from pydantic import BaseModel, Field

from utils.logger import logger


class PolicyCheckSchema(BaseModel):

    is_compliant: bool = Field(
        description=(
            "True if content complies with "
            "IRDAI underwriting and disclosure rules."
        )
    )

    policy_violation_reason: str = Field(
        description=(
            "Reason for rejection if non-compliant."
        )
    )


class PolicyEnforcer:
    """
    IRDAI Compliance Guardrail

    Blocks:
    - Guaranteed return claims
    - Non-disclosure advice
    - Insurance fraud
    - Fake documentation advice

    Allows:
    - Honest smoking disclosures
    - Medical disclosures
    - Insurance product questions
    - Financial underwriting questions
    """

    BLOCKED_PHRASES = [

        # ----------------------------------
        # Guaranteed Returns
        # ----------------------------------

        "guaranteed returns",
        "guaranteed market returns",
        "guaranteed ulip returns",
        "fixed investment returns",
        "risk free ulip",
        "guaranteed profit",

        # ----------------------------------
        # Concealment / Non-Disclosure
        # ----------------------------------

        "hide smoking history",
        "hide medical history",
        "hide tobacco usage",
        "hide health condition",

        "don't disclose smoking",
        "do not disclose smoking",

        "don't disclose medical condition",
        "do not disclose medical condition",

        "conceal smoking",
        "conceal medical history",

        "under report smoking",
        "underreport smoking",

        # ----------------------------------
        # Fraudulent Documents
        # ----------------------------------

        "fake medical records",
        "fake income proof",
        "fake itr",
        "fake form 16",
        "fake form16",

        # ----------------------------------
        # Insurance Fraud
        # ----------------------------------

        "insurance fraud",
        "forge medical records",
        "forge income proof"
    ]

    SAFE_DISCLOSURE_PHRASES = [

        "i smoke",
        "i occasionally smoke",
        "i am a smoker",
        "smoker",

        "tobacco user",
        "i use tobacco",

        "medical history",
        "family history",

        "diabetes",
        "hypertension",
        "blood pressure",

        "heart disease",

        "i drink",
        "alcohol consumption"
    ]

    def check_policy_compliance(
        self,
        query: str
    ) -> PolicyCheckSchema:

        if not query:

            return PolicyCheckSchema(
                is_compliant=True,
                policy_violation_reason=""
            )

        query_lower = query.lower().strip()

        # ----------------------------------
        # Allow Honest Disclosures
        # ----------------------------------

        for phrase in self.SAFE_DISCLOSURE_PHRASES:

            if phrase in query_lower:

                logger.info(
                    f"[IRDAI GUARDRAIL] "
                    f"Allowed disclosure detected: {phrase}"
                )

                return PolicyCheckSchema(
                    is_compliant=True,
                    policy_violation_reason=""
                )

        # ----------------------------------
        # Block Policy Violations
        # ----------------------------------

        for phrase in self.BLOCKED_PHRASES:

            if phrase in query_lower:

                logger.warning(
                    f"[IRDAI GUARDRAIL] "
                    f"Blocked phrase: {phrase}"
                )

                return PolicyCheckSchema(
                    is_compliant=False,
                    policy_violation_reason=(
                        f"IRDAI Compliance Violation: {phrase}"
                    )
                )

        # ----------------------------------
        # Default Allow
        # ----------------------------------

        return PolicyCheckSchema(
            is_compliant=True,
            policy_violation_reason=""
        )


policy_enforcer = PolicyEnforcer()