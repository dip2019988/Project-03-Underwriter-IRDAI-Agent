from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Premium MCP Service",
    version="1.0.0"
)


class MCPInvokeRequest(BaseModel):
    tool_name: str
    arguments: dict = {}


def calculate_premium(
    age,
    sum_assured,
    smoker=False
):

    base_rate = 0.005

    premium = (
        sum_assured * base_rate
    )

    premium *= (1 + age / 100)

    if smoker:
        premium *= 1.25

    return {
        "premium": round(premium, 2),
        "currency": "INR"
    }


@app.post("/mcp/invoke")
async def invoke_tool(request: MCPInvokeRequest):

    if request.tool_name != "calculate_premium":

        return {
            "error":
            f"Unknown tool: {request.tool_name}"
        }

    args = request.arguments

    result = calculate_premium(
        age=args.get("age"),
        sum_assured=args.get("sum_assured"),
        smoker=args.get("smoker", False)
    )

    return {
        "result": result
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }