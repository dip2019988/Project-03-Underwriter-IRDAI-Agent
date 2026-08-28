from typing import Any

import requests

from config.settings import settings
from utils.logger import logger


class RemoteMCPClient:
    """
    HTTP Client for Insurance MCP Services

    Connects LangGraph to:

    - BMI Service
    - HLV Service
    - Premium Service
    """

    def __init__(self):

        self.services = {

            "bmi":
                settings.MCP_BMI_URL,

            "hlv":
                settings.MCP_HLV_URL,

            "premium":
                settings.MCP_PREMIUM_URL
        }

    def call_mcp_service(
        self,
        service_key: str,
        tool_name: str,
        arguments: dict | None = None
    ) -> dict[str, Any]:

        if arguments is None:
            arguments = {}

        base_url = self.services.get(
            service_key
        )

        if not base_url:

            logger.error(
                f"[MCP CLIENT] Unknown service: {service_key}"
            )

            return {
                "error":
                    f"Service '{service_key}' not configured."
            }

        endpoint = f"{base_url}/mcp/invoke"

        payload = {
            "tool_name": tool_name,
            "arguments": arguments
        }

        try:

            logger.info(
                f"[MCP CLIENT] Calling {service_key}"
            )

            response = requests.post(
                endpoint,
                json=payload,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            logger.info(
                f"[MCP CLIENT] Success: "
                f"{response.status_code}"
            )

            return data.get(
                "result",
                data
            )

        except requests.exceptions.RequestException as e:

            logger.warning(
                f"[MCP CLIENT] Service unavailable: "
                f"{e!s}"
            )

            return {

                "status": "fallback",

                "message":
                    f"Service {service_key} unavailable"
            }


mcp_remote_client = RemoteMCPClient()