from graph.state import UnderwritingState
from services.mcp_client import mcp_remote_client
from utils.logger import logger


def mcp_execution_node(
    state: UnderwritingState
) -> dict:

    """
    Executes Insurance MCP Tools:
    - BMI Calculator
    - HLV Calculator
    - Premium Calculator
    """

    logger.info(
        "--- [NODE] Insurance MCP Tool Execution ---"
    )

    intent = state.get("intent", "GENERAL")

    visited = ["mcp_execution_node"]

    # --------------------------------------------------
    # HEALTH RISK -> BMI TOOL
    # --------------------------------------------------

    if intent == "HEALTH_RISK":

        logger.info(
            "[MCP NODE] Calling BMI Tool..."
        )

        result = mcp_remote_client.call_mcp_service(
            service_key="bmi",
            tool_name="calculate_bmi",
            arguments={
                "height_cm": state.get(
                    "medical_profile",
                    {}
                ).get("height_cm", 170),

                "weight_kg": state.get(
                    "medical_profile",
                    {}
                ).get("weight_kg", 70)
            }
        )

        return {
            "bmi_result": result,
            "visited_nodes": visited,
            "execution_logs": [
                "BMI MCP Tool Executed"
            ]
        }

    # --------------------------------------------------
    # FINANCIAL UNDERWRITING -> HLV TOOL
    # --------------------------------------------------

    elif intent == "FINANCIAL_UNDERWRITING":

        logger.info(
            "[MCP NODE] Calling HLV Tool..."
        )

        result = mcp_remote_client.call_mcp_service(
            service_key="hlv",
            tool_name="calculate_hlv",
            arguments={
                "annual_income":
                    state.get(
                        "financial_profile",
                        {}
                    ).get(
                        "annual_income",
                        1000000
                    ),

                "age":
                    state.get(
                        "customer_profile",
                        {}
                    ).get(
                        "age",
                        30
                    ),

                "existing_cover":
                    state.get(
                        "financial_profile",
                        {}
                    ).get(
                        "existing_cover",
                        0
                    )
            }
        )

        return {
            "hlv_result": result,
            "visited_nodes": visited,
            "execution_logs": [
                "HLV MCP Tool Executed"
            ]
        }

    # --------------------------------------------------
    # LIFESTYLE RISK -> PREMIUM TOOL
    # --------------------------------------------------

    elif intent == "LIFESTYLE_RISK":

        logger.info(
            "[MCP NODE] Calling Premium Tool..."
        )

        result = mcp_remote_client.call_mcp_service(
            service_key="premium",
            tool_name="calculate_premium",
            arguments={

                "age":
                    state.get(
                        "customer_profile",
                        {}
                    ).get(
                        "age",
                        30
                    ),

                "sum_assured":
                    state.get(
                        "financial_profile",
                        {}
                    ).get(
                        "requested_cover",
                        10000000
                    ),

                "smoker":
                    state.get(
                        "medical_profile",
                        {}
                    ).get(
                        "smoker",
                        False
                    )
            }
        )

        return {
            "premium_quote": result,
            "visited_nodes": visited,
            "execution_logs": [
                "Premium MCP Tool Executed"
            ]
        }

    return {
        "visited_nodes": visited,
        "execution_logs": [
            "No MCP tool required"
        ]
    }