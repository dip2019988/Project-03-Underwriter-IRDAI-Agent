from graph.state import UnderwritingState

from services.vector_store_service import insurance_vector_store

from utils.logger import logger


def fallback_kb_node(
    state: UnderwritingState
) -> dict:

    logger.info(
        "--- [NODE] Insurance Knowledge Base Agent ---"
    )

    query = state.get(
        "sanitized_query",
        state.get(
            "raw_query",
            ""
        )
    )

    retrieved_docs = (
        insurance_vector_store
        .similarity_search(
            query=query,
            k=5
        )
    )

    formatted_docs = []

    for doc in retrieved_docs:

        formatted_docs.append(
            {
                "title":
                    doc.metadata.get(
                        "title"
                    ),

                "category":
                    doc.metadata.get(
                        "category"
                    ),

                "id":
                    doc.metadata.get(
                        "id"
                    ),

                "content":
                    doc.page_content
            }
        )

    logger.info(
        f"[FAISS] Retrieved "
        f"{len(formatted_docs)} "
        f"documents."
    )

    return {

        "retrieved_docs":
            formatted_docs,

        "visited_nodes": [
            "fallback_kb_node"
        ],

        "execution_logs": [
            (
                f"Retrieved "
                f"{len(formatted_docs)} "
                f"documents via FAISS"
            )
        ]
    }