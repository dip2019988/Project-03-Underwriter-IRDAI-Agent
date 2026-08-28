from graph.state import UnderwritingState
from services.mcp_client import mcp_remote_client
from utils.logger import logger


def mcp_execution_node(
    state: UnderwritingState
) -> dict:

    """
    Executes Insurance MCP Tools.

    HEALTH_RISK
        -> BMI

    FINANCIAL_UNDERWRITING
        -> HLV
        -> Premium

    LIFESTYLE_RISK
        -> BMI (if available)
        -> Premium
    """

    logger.info(
        "--- [NODE] Insurance MCP Tool Execution ---"
    )

    intent = state.get(
        "intent",
        "GENERAL"
    )

    customer_profile = state.get(
        "customer_profile",
        {}
    )

    financial_profile = state.get(
        "financial_profile",
        {}
    )

    medical_profile = state.get(
        "medical_profile",
        {}
    )

    contains_ulip_request = state.get(
        "contains_ulip_request",
        False
    )

    visited = ["mcp_execution_node"]

    bmi_result = {}
    hlv_result = {}
    premium_quote = {}
    ulip_illustration = {}

    execution_logs = []

    # --------------------------------------------------
    # HEALTH RISK
    # --------------------------------------------------

    if intent == "HEALTH_RISK":

        height_cm = medical_profile.get(
            "height_cm",
            0
        )

        weight_kg = medical_profile.get(
            "weight_kg",
            0
        )

        if height_cm and weight_kg:

            logger.info(
                "[MCP NODE] Calling BMI Tool..."
            )

            bmi_result = (
                mcp_remote_client.call_mcp_service(
                    service_key="bmi",
                    tool_name="calculate_bmi",
                    arguments={
                        "height_cm": height_cm,
                        "weight_kg": weight_kg
                    }
                )
            )

            execution_logs.append(
                "BMI MCP Tool Executed"
            )

    # --------------------------------------------------
    # FINANCIAL UNDERWRITING
    # --------------------------------------------------

    elif intent == "FINANCIAL_UNDERWRITING":

        height_cm = medical_profile.get(
            "height_cm",
            0
        )

        weight_kg = medical_profile.get(
            "weight_kg",
            0
        )

        if height_cm and weight_kg:

            logger.info(
                "[MCP NODE] Calling BMI Tool..."
            )

            bmi_result = (
                mcp_remote_client.call_mcp_service(
                    service_key="bmi",
                    tool_name="calculate_bmi",
                    arguments={
                        "height_cm": height_cm,
                        "weight_kg": weight_kg
                    }
                )
            )

            execution_logs.append(
                "BMI MCP Tool Executed"
            )

        logger.info(
            "[MCP NODE] Calling HLV Tool..."
        )

        hlv_result = (
            mcp_remote_client.call_mcp_service(
                service_key="hlv",
                tool_name="calculate_hlv",
                arguments={
                    "annual_income":
                        financial_profile.get(
                            "annual_income",
                            0
                        ),

                    "age":
                        customer_profile.get(
                            "age",
                            0
                        ),

                    "existing_cover":
                        financial_profile.get(
                            "existing_cover",
                            0
                        )
                }
            )
        )

        execution_logs.append(
            "HLV MCP Tool Executed"
        )

        logger.info(
            "[MCP NODE] Calling Premium Tool..."
        )

        premium_quote = (
            mcp_remote_client.call_mcp_service(
                service_key="premium",
                tool_name="calculate_premium",
                arguments={
                    "age":
                        customer_profile.get(
                            "age",
                            0
                        ),

                    "sum_assured":
                        financial_profile.get(
                            "requested_cover",
                            0
                        ),

                    "smoker":
                        medical_profile.get(
                            "smoker",
                            False
                        )
                }
            )
        )

        execution_logs.append(
            "Premium MCP Tool Executed"
        )

        # ----------------------------------
        # ULIP Illustration
        # ----------------------------------

        if contains_ulip_request:

            from nodes.knowledge_node import extract_investment_amount

            investment = (
                extract_investment_amount(
                    state.get(
                        "sanitized_query",
                        ""
                    )
                )
            )

            if investment > 0:

                ulip_illustration = {

                    "investment_amount":
                        investment,

                    "illustration_4_percent":
                        investment * 1.04,

                    "illustration_8_percent":
                        investment * 1.08,

                    "regulatory_disclosure":
                        (
                            "Illustrative only. "
                            "Market-linked returns "
                            "are not guaranteed."
                        )
                }

                execution_logs.append(
                    "ULIP Illustration Generated"
                )    

    # --------------------------------------------------
    # LIFESTYLE RISK
    # --------------------------------------------------

    elif intent == "LIFESTYLE_RISK":

        height_cm = medical_profile.get(
            "height_cm",
            0
        )

        weight_kg = medical_profile.get(
            "weight_kg",
            0
        )

        if height_cm and weight_kg:

            logger.info(
                "[MCP NODE] Calling BMI Tool..."
            )

            bmi_result = (
                mcp_remote_client.call_mcp_service(
                    service_key="bmi",
                    tool_name="calculate_bmi",
                    arguments={
                        "height_cm": height_cm,
                        "weight_kg": weight_kg
                    }
                )
            )

            execution_logs.append(
                "BMI MCP Tool Executed"
            )

        logger.info(
            "[MCP NODE] Calling Premium Tool..."
        )

        premium_quote = (
            mcp_remote_client.call_mcp_service(
                service_key="premium",
                tool_name="calculate_premium",
                arguments={
                    "age":
                        customer_profile.get(
                            "age",
                            0
                        ),

                    "sum_assured":
                        financial_profile.get(
                            "requested_cover",
                            0
                        ),

                    "smoker":
                        medical_profile.get(
                            "smoker",
                            False
                        )
                }
            )
        )

        execution_logs.append(
            "Premium MCP Tool Executed"
        )

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    if not execution_logs:

        execution_logs.append(
            "No MCP Tool Required"
        )

    return {

        "bmi_result":
            bmi_result,

        "hlv_result":
            hlv_result,

        "premium_quote":
            premium_quote,

        "ulip_illustration":
            ulip_illustration,

        "visited_nodes":
            visited,

        "execution_logs":
            execution_logs
    }