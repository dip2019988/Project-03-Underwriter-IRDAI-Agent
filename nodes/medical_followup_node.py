from graph.state import UnderwritingState
from utils.logger import logger


def medical_followup_node(
    state: UnderwritingState
) -> dict:

    logger.info(
        "--- [NODE] Medical Follow-Up Assessment ---"
    )

    query = state.get(
        "sanitized_query",
        ""
    ).lower()

    follow_up_questions = []

    # Asthma

    if "asthma" in query:

        follow_up_questions.extend([
            (
                "Have you ever been hospitalized "
                "due to asthma?"
            ),
            (
                "Do you currently use inhalers?"
            ),
            (
                "Have you used steroid medication "
                "for asthma treatment?"
            )
        ])

    # Diabetes

    if "diabetes" in query:

        follow_up_questions.extend([
            (
                "How long have you had diabetes?"
            ),
            (
                "Are you taking insulin?"
            ),
            (
                "Have you experienced diabetes "
                "related complications?"
            )
        ])

    # Hypertension

    if (
        "hypertension" in query
        or
        "high blood pressure" in query
    ):

        follow_up_questions.extend([
            (
                "How long have you had hypertension?"
            ),
            (
                "Are you currently taking medication?"
            ),
            (
                "Have you ever been hospitalized "
                "for hypertension?"
            )
        ])

    return {

        "follow_up_questions":
            follow_up_questions,

        "visited_nodes": [
            "medical_followup_node"
        ],

        "execution_logs": [
            "Generated medical follow-up questions"
        ]
    }