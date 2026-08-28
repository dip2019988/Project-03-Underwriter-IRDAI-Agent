import json
import re

from config.settings import settings
from graph.state import UnderwritingState
from utils.logger import logger


def tokenize(text: str) -> set:

    text = text.lower()

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text
    )

    stop_words = {
        "the",
        "and",
        "or",
        "is",
        "are",
        "a",
        "an",
        "my",
        "i",
        "me",
        "want",
        "need",
        "for",
        "with",
        "of",
        "to"
    }

    return {
        w for w in words
        if w not in stop_words
    }


def fallback_kb_node(
    state: UnderwritingState
) -> dict:

    """
    Insurance Regulatory RAG Node

    Retrieves:
    - IRDAI Regulations
    - Underwriting Guidelines
    - HLV Rules
    - Smoking Rules
    - Product Information
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
        state.get(
            "raw_query",
            ""
        )
    )

    query_tokens = tokenize(query)

    scored_documents = []

    for doc in docs:

        content = doc.get(
            "content",
            ""
        )

        title = doc.get(
            "title",
            ""
        )

        combined_text = (
            f"{title} {content}"
        )

        doc_tokens = tokenize(
            combined_text
        )

        overlap = len(
            query_tokens.intersection(
                doc_tokens
            )
        )

        if overlap > 0:

            scored_documents.append(
                (
                    overlap,
                    doc
                )
            )

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    matched_docs = [
        doc
        for _, doc
        in scored_documents[:5]
    ]

    # --------------------------------------------------
    # Regulatory Fallback
    # --------------------------------------------------

    if not matched_docs:

        logger.warning(
            "[RAG] No keyword match. "
            "Returning top regulatory docs."
        )

        matched_docs = docs[:5]

    logger.info(
        f"[RAG] Retrieved "
        f"{len(matched_docs)} documents."
    )

    return {

        "retrieved_docs":
            matched_docs,

        "visited_nodes": [
            "fallback_kb_node"
        ],

        "execution_logs": [
            (
                f"Retrieved "
                f"{len(matched_docs)} "
                "insurance documents"
            )
        ]
    }