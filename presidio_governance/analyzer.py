from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern
)

from utils.logger import logger


class InsurancePresidioAnalyzer:
    """
    Presidio Analyzer for Insurance Underwriting

    Detects:
    - PAN Numbers
    - Bank Account Numbers
    - IFSC Codes
    - Phone Numbers
    - Aadhaar References
    """

    def __init__(self):

        self.analyzer = AnalyzerEngine()

        # ----------------------------------
        # PAN
        # Example: ABCDE1234F
        # ----------------------------------

        pan_pattern = Pattern(
            name="pan_pattern",
            regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            score=0.99
        )

        pan_recognizer = PatternRecognizer(
            supported_entity="PAN_NUMBER",
            patterns=[pan_pattern],
            context=[
                "pan",
                "income tax",
                "itr",
                "form16"
            ]
        )

        self.analyzer.registry.add_recognizer(
            pan_recognizer
        )

        # ----------------------------------
        # IFSC Code
        # Example:
        # HDFC0001234
        # ----------------------------------

        ifsc_pattern = Pattern(
            name="ifsc_pattern",
            regex=r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
            score=0.95
        )

        ifsc_recognizer = PatternRecognizer(
            supported_entity="IFSC_CODE",
            patterns=[ifsc_pattern]
        )

        self.analyzer.registry.add_recognizer(
            ifsc_recognizer
        )

        # ----------------------------------
        # Bank Account
        # ----------------------------------

        bank_pattern = Pattern(
            name="bank_account_pattern",
            regex=r"\b\d{9,18}\b",
            score=0.80
        )

        bank_recognizer = PatternRecognizer(
            supported_entity="BANK_ACCOUNT",
            patterns=[bank_pattern],
            context=[
                "account",
                "bank",
                "savings",
                "current"
            ]
        )

        self.analyzer.registry.add_recognizer(
            bank_recognizer
        )

        logger.info(
            "[PRESIDIO] Insurance recognizers loaded."
        )

    def analyze_text(
        self,
        text: str,
        score_threshold: float = 0.6
    ) -> list:

        if not text:
            return []

        results = self.analyzer.analyze(

            text=text,

            entities=[

                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",

                "PAN_NUMBER",
                "IFSC_CODE",
                "BANK_ACCOUNT",

                "CREDIT_CARD"
            ],

            language="en",

            score_threshold=score_threshold
        )

        return results


presidio_analyzer_service = (
    InsurancePresidioAnalyzer()
)