from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="HLV MCP Service",
    version="1.0.0"
)


class MCPInvokeRequest(BaseModel):
    tool_name: str
    arguments: dict = {}


def calculate_hlv(
    annual_income,
    age,
    existing_cover
):

    if age < 35:
        multiplier = 20

    elif age < 45:
        multiplier = 15

    else:
        multiplier = 10

    max_cover = (
        annual_income * multiplier
    ) - existing_cover

    return {
        "multiplier": multiplier,
        "maximum_eligible_hlv": max_cover
    }


@app.post("/mcp/invoke")
async def invoke_tool(request: MCPInvokeRequest):

    if request.tool_name != "calculate_hlv":

        return {
            "error":
            f"Unknown tool: {request.tool_name}"
        }

    args = request.arguments

    result = calculate_hlv(
        annual_income=args.get("annual_income"),
        age=args.get("age"),
        existing_cover=args.get("existing_cover", 0)
    )

    return {
        "result": result
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }