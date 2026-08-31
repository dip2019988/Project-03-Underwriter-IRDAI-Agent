import re
import warnings

from mem0 import Memory

from config.settings import settings
from utils.logger import logger

warnings.filterwarnings(
    "ignore",
    category=ResourceWarning
)


class Mem0Service:
    """
    Insurance Customer Memory Service

    Stores:

    - Family details
    - Dependents
    - Smoking disclosures
    - Medical conditions
    - Financial goals
    - Risk tolerance
    """

    def __init__(self):

        try:

            mem0_config = {

                "llm": {

                    "provider": "openai",

                    "config": {

                        "model":
                            settings.OPENAI_MODEL_NAME
                            if settings.OPENAI_MODEL_NAME != "gpt-5-mini"
                            else "gpt-4o-mini",

                        "api_key":
                            settings.OPENAI_API_KEY
                    }
                }
            }

            if settings.MEM0_API_KEY:
                mem0_config["api_key"] = (
                    settings.MEM0_API_KEY
                )

            self.memory = Memory.from_config(
                mem0_config
            )

            logger.info(
                "[MEM0] Insurance Memory Service initialized."
            )

        except Exception as e:

            logger.warning(
                f"[MEM0] Initialization issue: {e!s}"
            )

            self.memory = None

    def get_customer_memories(
        self,
        customer_id: str
    ) -> list[str]:

        if not self.memory:
            return []

        try:

            results = self.memory.get_all(
                filters={"user_id": customer_id}
            )

            memories = []

            if isinstance(results, list):
                for item in results:
                    if (
                        isinstance(item, dict)
                        and "memory" in item
                    ):
                        memories.append(
                            item["memory"]
                        )

            elif (
                isinstance(results, dict)
                and "results" in results
            ):
                memories = [
                    m.get("memory", "")
                    for m in results["results"]
                ]

            logger.info(
                f"[MEM0] Retrieved {len(memories)} memories "
                f"for customer '{customer_id}'."
            )

            return memories

        except Exception as e:

            logger.error(
                f"[MEM0] Failed to fetch memories: "
                f"{e!s}"
            )

            return []

    def sanitize_memory_text(
        self,
        text: str
    ) -> str:

        if not text:
            return text

        # PAN
        text = re.sub(
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            "<PAN_REDACTED>",
            text
        )

        # Aadhaar
        text = re.sub(
            r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "<AADHAAR_REDACTED>",
            text
        )

        # IFSC
        text = re.sub(
            r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
            "<IFSC_REDACTED>",
            text
        )

        # Phone
        text = re.sub(
            r"\b\d{10}\b",
            "<PHONE_REDACTED>",
            text
        )

        # Email
        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "<EMAIL_REDACTED>",
            text
        )

        # Credit cards
        text = re.sub(
            r"\b(?:\d[\s-]?){13,19}\b",
            "<CARD_REDACTED>",
            text
        )

        # Bank account numbers
        text = re.sub(
            r"\b(?:\d[\s-]?){11,18}\b",
            "<BANK_ACCOUNT_REDACTED>",
            text
        )

        # Salary values
        text = re.sub(
            r"₹\s?[\d,]+(?:\.\d+)?",
            "<SALARY_REDACTED>",
            text,
            flags=re.IGNORECASE
        )

        # Income expressions
        text = re.sub(
            r"\b\d+(?:\.\d+)?\s*(lakh|lakhs|crore|crores)\b",
            "<INCOME_REDACTED>",
            text,
            flags=re.IGNORECASE
        )

        # Employer references
        text = re.sub(
            r"(employer|company|organization)\s*:\s*[^\n]+",
            "<EMPLOYER_REDACTED>",
            text,
            flags=re.IGNORECASE
        )

        return text

        
    def add_customer_memory(
        self,
        customer_id: str,
        interaction: str
    ):

        if not self.memory:
            return

        try:

            sanitized_interaction = (
                self.sanitize_memory_text(
                    interaction
                )
            )

            self.memory.add(
                sanitized_interaction,
                user_id=customer_id
            )

            logger.info(
                "[MEM0] Customer memory saved."
            )

        except Exception as e:

            logger.error(
                f"[MEM0] Save failed: {e!s}"
            )

    def close(self):
        """
        Gracefully close memory resources.

        This helps shut down Mem0/Qdrant
        before Python interpreter cleanup.
        """

        if self.memory is None:
            return

        try:

            # Some Mem0 versions expose
            # a close() method.
            if hasattr(
                self.memory,
                "close"
            ):

                self.memory.close()

            logger.info(
                "[MEM0] Memory service closed."
            )

        except Exception as e:

            logger.warning(
                f"[MEM0] Close warning: {e!s}"
            )


mem0_service = Mem0Service()