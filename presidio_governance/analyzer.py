from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer

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

        salary_pattern = Pattern(
            name="salary_pattern",
            regex=r"₹\s?\d[\d,]*",
            score=0.85
        )

        # ----------------------------------
        # Salary
        # Example: ₹18,00,000
        # ----------------------------------
        
        salary_recognizer = PatternRecognizer(
            supported_entity="SALARY_AMOUNT",
            patterns=[salary_pattern],
            context=[
                "salary",
                "annual income",
                "gross salary",
                "form 16",
                "form16",
                "itr"
            ]
        )

        self.analyzer.registry.add_recognizer(
            salary_recognizer
        )

        # ----------------------------------
        # Employer
        # Example: ABC Technologies Pvt Ltd
        # ----------------------------------

        employer_pattern = Pattern(
            name="employer_pattern",
            regex=r"\b[A-Z][A-Za-z& ]+(?:Pvt Ltd|Private Limited|Ltd|Limited)\b",
            score=0.90
        )

        employer_recognizer = PatternRecognizer(
            supported_entity="EMPLOYER_NAME",
            patterns=[employer_pattern],
            context=[
                "employer",
                "company",
                "organisation",
                "organization",
                "form 16",
                "salary"
            ]
        )

        self.analyzer.registry.add_recognizer(
            employer_recognizer
        )

        # ----------------------------------
        # Address
        # Example: B-1204, Green Valley Apartments, Powai, Mumbai 400076

        # ----------------------------------

        address_pattern = Pattern(
            name="address_pattern",
            regex=(
                r"\b[A-Za-z]?\-?\d+"
                r"[A-Za-z0-9\-/, ]*"
                r"(?:Road|Rd|Street|St|Avenue|Ave|"
                r"Apartment|Apartments|Tower|Block)"
                r"[A-Za-z0-9,\s\-]*"
                r"\d{6}\b"
            ),
            score=0.90
        )

        address_recognizer = PatternRecognizer(
            supported_entity="ADDRESS",
            patterns=[address_pattern],
            context=[
                "address",
                "residence",
                "resident",
                "flat",
                "tower"
            ]
        )

        self.analyzer.registry.add_recognizer(
            address_recognizer
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
            regex=r"\b\d{11,18}\b",
            score=0.80
        )

        bank_spaced_pattern = Pattern(
            name="bank_account_pattern_spaced",
            regex=r"\b\d{4}\s\d{4}\s\d{5,8}\b",
            score=0.60
        )

        bank_recognizer = PatternRecognizer(
            supported_entity="BANK_ACCOUNT",
            patterns=[
                bank_pattern,
                bank_spaced_pattern
            ],
            context=[
                "account",
                "bank",
                "savings",
                "current",
                "account number"
            ]
        )

        self.analyzer.registry.add_recognizer(
            bank_recognizer
        )

        # ----------------------------------
        # Aadhaar
        # Example:
        # 1234-5678-9012
        # 1234 5678 9012
        # 123456789012
        # ----------------------------------

        aadhaar_pattern = Pattern(
            name="aadhaar_pattern",
            regex=r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            score=1.0
        )

        aadhaar_recognizer = PatternRecognizer(
            supported_entity="AADHAAR_NUMBER",
            patterns=[aadhaar_pattern],
            context=[
                "aadhaar",
                "aadhar",
                "uid",
                "uidai"
            ]
        )

        self.analyzer.registry.add_recognizer(
            aadhaar_recognizer
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
                "AADHAAR_NUMBER",
                "IFSC_CODE",
                "BANK_ACCOUNT",

                "CREDIT_CARD",
                "SALARY_AMOUNT",
                "EMPLOYER_NAME",
                "ADDRESS",
            ],

            language="en",

            score_threshold=score_threshold
        )

                # ----------------------------------
        # Resolve overlapping detections
        # Prefer Aadhaar over Bank Account
        # ----------------------------------

        priority = {
            "PAN_NUMBER": 5,
            "AADHAAR_NUMBER": 4,
            "IFSC_CODE": 3,
            "EMAIL_ADDRESS": 2,
            "PHONE_NUMBER": 2,
            "BANK_ACCOUNT": 1,
            "CREDIT_CARD": 1,
            "SALARY_AMOUNT": 2,
            "EMPLOYER_NAME": 2,
            "ADDRESS": 2,
        }


        filtered_results = []


        for result in results:

            is_duplicate = False

            for existing in filtered_results:

                overlaps = (
                    result.start < existing.end
                    and
                    result.end > existing.start
                )

                if overlaps:

                    existing_priority = priority.get(
                        existing.entity_type,
                        0
                    )

                    current_priority = priority.get(
                        result.entity_type,
                        0
                    )

                    if current_priority > existing_priority:

                        filtered_results.remove(
                            existing
                        )

                        filtered_results.append(
                            result
                        )

                    is_duplicate = True
                    break

            if not is_duplicate:

                filtered_results.append(
                    result
                )

        return filtered_results


presidio_analyzer_service = (
    InsurancePresidioAnalyzer()
)