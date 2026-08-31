import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from services.vector_store_service import (
    insurance_vector_store
)

test_queries = [

    "What is Section 45?",

    "Show ULIP returns illustration",

    "What is smoker classification?",

    "My father had bypass surgery",

    "I work in mining industry"
]

print("\n========================")
print("FAISS RAG VALIDATION")
print("========================\n")

for query in test_queries:

    print(f"\nQUERY: {query}")

    results = (
        insurance_vector_store
        .similarity_search(
            query=query,
            k=3
        )
    )

    print("\nTOP RESULTS:\n")

    for doc in results:

        print(
            f"ID: "
            f"{doc.metadata.get('id')}"
        )

        print(
            f"CATEGORY: "
            f"{doc.metadata.get('category')}"
        )

        print(
            f"TITLE: "
            f"{doc.metadata.get('title')}"
        )

        print(
            f"CONTENT: "
            f"{doc.page_content}"
        )

        print("-" * 50)