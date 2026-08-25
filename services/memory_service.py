import warnings
from typing import List

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
                f"[MEM0] Initialization issue: {str(e)}"
            )

            self.memory = None

    def get_customer_memories(
        self,
        customer_id: str
    ) -> List[str]:

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
                f"{str(e)}"
            )

            return []

    def add_customer_memory(
        self,
        customer_id: str,
        interaction: str
    ):

        if not self.memory:
            return

        try:

            self.memory.add(
                interaction,
                user_id=customer_id
            )

            logger.info(
                "[MEM0] Customer memory saved."
            )

        except Exception as e:

            logger.error(
                f"[MEM0] Save failed: {str(e)}"
            )

    def close(self):
        pass


mem0_service = Mem0Service()