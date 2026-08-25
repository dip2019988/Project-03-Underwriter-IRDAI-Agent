import json

from graph.state import UnderwritingState
from config.settings import settings
from utils.logger import logger


def auth_analysis_node(
    state: UnderwritingState
) -> dict:

    """
    Customer Profile & Financial Underwriting Node

    Retrieves:
    - HLV Rules
    - Financial Eligibility Rules
    - Underwriting Guidelines
    """

    logger.info(
        "--- [NODE] Customer Profile Analysis Agent ---"
    )

    docs = []

    if settings.KB_FILE_PATH.exists():

        with open(
            settings.KB_FILE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            kb = json.load(f)

            docs = [

                item

                for item in kb

                if item.get("category") in [

                    "FINANCIAL_UNDERWRITING",
                    "HLV",
                    "TERM_PLAN",
                    "UNDERWRITING_RULES"
                ]
            ]

    return {

        "retrieved_docs": docs,

        "visited_nodes": [
            "auth_analysis_node"
        ],

        "execution_logs": [
            "Retrieved underwriting eligibility guidelines"
        ]
    }