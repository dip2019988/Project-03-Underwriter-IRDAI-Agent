import re
from typing import Tuple

from utils.logger import logger


class SchemaValidator:
    """
    Insurance Input and Output Validator
    """

    def __init__(self):

        self.forbidden_patterns = [

            r"hide\s+smoking",

            r"hide\s+medical",

            r"don't\s+disclose\s+smoking",

            r"do\s+not\s+disclose\s+smoking",

            r"fake\s+itr",

            r"fake\s+form\s*16",

            r"fake\s+medical",

            r"fake\s+income\s+proof"
        ]

    def validate_input_query(
        self,
        query: str
    ) -> Tuple[bool, str]:

        if not query or not query.strip():
            return (
                False,
                "Input query cannot be empty."
            )

        if len(query) > 5000:
            return (
                False,
                "Input exceeds maximum length."
            )

        for pattern in self.forbidden_patterns:

            if re.search(
                pattern,
                query,
                re.IGNORECASE
            ):

                logger.warning(
                    f"[SCHEMA VALIDATOR] "
                    f"Forbidden pattern detected: "
                    f"{pattern}"
                )

                return (
                    False,
                    "Query contains prohibited content."
                )

        return (
            True,
            "Valid"
        )

    def validate_underwriting_output(
        self,
        result: dict
    ) -> Tuple[bool, str]:

        required_fields = [

            "proposal_id",

            "financial_underwriting",

            "medical_and_lifestyle_risk",

            "pre_underwriting_decision",

            "regulatory_and_compliance"
        ]

        for field in required_fields:

            if field not in result:

                return (
                    False,
                    f"Missing field: {field}"
                )

        return (
            True,
            "Valid"
        )


schema_validator = SchemaValidator()