import json

from graph.state import UnderwritingState
from config.settings import settings
from utils.logger import logger


def fallback_kb_node(
    state: UnderwritingState
) -> dict:

    """
    Insurance Regulatory and Product RAG Node

    Loads:
    - IRDAI Regulations
    - Term Plan Rules
    - ULIP Rules
    - Underwriting Guidelines
    """

    logger.info(
        "--- [NODE] Insurance Knowledge Base Agent ---"
    )

    docs = []

    if settings.KB_FILE_PATH.exists():

        with open(
            settings.KB_FILE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            docs = json.load(f)

    query = state.get(
        "sanitized_query",
        ""
    ).lower()

    matched_docs = []

    for doc in docs:

        content = doc.get(
            "content",
            ""
        ).lower()

        if query in content:
            matched_docs.append(doc)

    if not matched_docs:
        matched_docs = docs[:3]

    return {

        "retrieved_docs": matched_docs,

        "visited_nodes": [
            "fallback_kb_node"
        ],

        "execution_logs": [
            "Insurance RAG lookup completed"
        ]
    }