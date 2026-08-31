from nodes.kb_node import fallback_kb_node


def test_section_45_rag_retrieval():
    """
    Test Pack 13

    Verify that a Section 45 query
    retrieves the correct regulatory
    documents from FAISS.
    """

    state = {
        "raw_query":
            "What is Section 45 of the Insurance Act?",

        "sanitized_query":
            "What is Section 45 of the Insurance Act?"
    }

    result = (
        fallback_kb_node(
            state
        )
    )

    retrieved_docs = (
        result.get(
            "retrieved_docs",
            []
        )
    )

    assert (
        len(retrieved_docs)
        > 0
    )

    # Top result should be
    # Section 45 guidance.

    assert (
        retrieved_docs[0]["id"]
        == "IRDAI-001"
    )

    assert (
        "Section 45"
        in
        retrieved_docs[0]["title"]
    )