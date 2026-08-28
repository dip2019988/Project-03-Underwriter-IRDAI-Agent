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

    BLOCKED_PHRASES = [

        # Guaranteed Returns

        "guaranteed returns",
        "guaranteed market returns",
        "guaranteed ulip returns",
        "fixed investment returns",
        "risk free ulip",
        "guaranteed profit",

        # Non Disclosure

        "hide smoking history",
        "hide smoking habit",
        "hide my smoking habit",

        "hide medical history",
        "hide tobacco usage",
        "hide health condition",

        "don't disclose smoking",
        "do not disclose smoking",

        "don't disclose medical condition",
        "do not disclose medical condition",

        "conceal smoking",
        "conceal smoking habit",
        "conceal medical history",

        "under report smoking",
        "underreport smoking",

        # Fraud

        "fake medical records",
        "fake income proof",
        "fake itr",
        "fake form 16",
        "fake form16",

        "insurance fraud",
        "forge medical records",
        "forge income proof"
    ]

    FRAUD_PATTERNS = [

        "can i hide",
        "should i hide",

        "can i conceal",
        "should i conceal",

        "avoid disclosing",
        "avoid disclosure",

        "not disclose",

        "without disclosing",

        "how do i hide",
        "how can i hide",

        "how do i conceal",
        "how can i conceal"
    ]

    SAFE_DISCLOSURE_PHRASES = [

        "i smoke",
        "i occasionally smoke",
        "i am a smoker",

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
        # BLOCK FIRST
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
        # Fraud Intent Patterns
        # ----------------------------------

        smoking_keywords = [
            "smoking",
            "smoker",
            "tobacco"
        ]

        medical_keywords = [
            "medical",
            "health condition",
            "medical history"
        ]

        for pattern in self.FRAUD_PATTERNS:

            if pattern in query_lower:

                for keyword in (
                    smoking_keywords
                    + medical_keywords
                ):

                    if keyword in query_lower:

                        reason = (
                            f"Attempt to conceal "
                            f"{keyword}"
                        )

                        logger.warning(
                            f"[IRDAI GUARDRAIL] "
                            f"{reason}"
                        )

                        return PolicyCheckSchema(
                            is_compliant=False,
                            policy_violation_reason=
                            reason
                        )

        # ----------------------------------
        # Honest Disclosure
        # ----------------------------------

        for phrase in self.SAFE_DISCLOSURE_PHRASES:

            if phrase in query_lower:

                logger.info(
                    f"[IRDAI GUARDRAIL] "
                    f"Allowed disclosure detected: "
                    f"{phrase}"
                )

                return PolicyCheckSchema(
                    is_compliant=True,
                    policy_violation_reason=""
                )

        # ----------------------------------
        # Allow Normal Queries
        # ----------------------------------

        return PolicyCheckSchema(
            is_compliant=True,
            policy_violation_reason=""
        )


policy_enforcer = PolicyEnforcer()