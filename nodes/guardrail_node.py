from graph.state import UnderwritingState

from presidio_governance.anonymizer import (
    presidio_anonymizer_service
)

from presidio_governance.rehydrator import (
    presidio_rehydrator_service
)

from guardrails.schema_validator import (
    schema_validator
)

from guardrails.injection_detector import (
    injection_detector
)

from guardrails.policy_enforcer import (
    policy_enforcer
)

from utils.logger import logger


def input_guardrail_node(
    state: UnderwritingState
) -> dict:

    """
    Insurance Pre-Processing Guardrail

    1. Input Validation
    2. Prompt Injection Detection
    3. Presidio PII Redaction
    4. IRDAI Compliance Validation
    """

    logger.info(
        "--- [GUARDRAIL] Insurance Input Validation ---"
    )

    raw_query = state.get(
        "raw_query",
        ""
    )

    # -----------------------------------------
    # Input Validation
    # -----------------------------------------

    is_valid, message = (
        schema_validator
        .validate_input_query(raw_query)
    )

    if not is_valid:

        return {

            "guardrail_passed": False,

            "guardrail_violation_reason":
                f"Input Validation Failed: {message}",

            "solution":
                f"⛔ Input rejected: {message}",

            "confidence_score": 100,

            "visited_nodes": [
                "input_guardrail_node"
            ],

            "execution_logs": [
                f"Input validation failed: {message}"
            ]
        }

    # -----------------------------------------
    # Prompt Injection Detection
    # -----------------------------------------

    if injection_detector.is_injection_attack(
        raw_query
    ):

        return {

            "guardrail_passed": False,

            "guardrail_violation_reason":
                "Prompt Injection Attempt Detected",

            "solution":
                "⛔ Security violation detected.",

            "confidence_score": 100,

            "visited_nodes": [
                "input_guardrail_node"
            ],

            "execution_logs": [
                "Prompt injection blocked"
            ]
        }

    # -----------------------------------------
    # Presidio Anonymization
    # -----------------------------------------

    sanitized_query, token_map = (
        presidio_anonymizer_service
        .anonymize_and_map(raw_query)
    )

    # -----------------------------------------
    # IRDAI Compliance Check
    # -----------------------------------------

    policy_result = (
        policy_enforcer
        .check_policy_compliance(
            sanitized_query
        )
    )

    if not policy_result.is_compliant:

        return {

            "guardrail_passed": False,

            "guardrail_violation_reason":
                policy_result.policy_violation_reason,

            "solution":
                f"⛔ Compliance Failure: "
                f"{policy_result.policy_violation_reason}",

            "confidence_score": 100,

            "visited_nodes": [
                "input_guardrail_node"
            ],

            "execution_logs": [
                policy_result.policy_violation_reason
            ]
        }

    return {

        "guardrail_passed": True,

        "guardrail_violation_reason": "",

        "sanitized_query":
            sanitized_query,

        "presidio_token_map":
            token_map,

        "visited_nodes": [
            "input_guardrail_node"
        ],

        "execution_logs": [
            "Insurance guardrail passed"
        ]
    }


def output_guardrail_node(
    state: UnderwritingState
) -> dict:

    logger.info(
        "--- [GUARDRAIL] Output Rehydration ---"
    )

    final_solution = (
        presidio_rehydrator_service
        .rehydrate_text(
            state.get(
                "solution",
                ""
            ),
            state.get(
                "presidio_token_map",
                {}
            )
        )
    )

    updated_state = dict(state)

    updated_state["solution"] = (
        final_solution
    )

    updated_state["visited_nodes"] = [
        "output_guardrail_node"
    ]

    updated_state["execution_logs"] = [
        "Proposal rehydrated"
    ]

    return updated_state