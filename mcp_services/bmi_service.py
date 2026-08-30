from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="BMI MCP Service",
    version="1.0.0"
)


class MCPInvokeRequest(BaseModel):
    tool_name: str
    arguments: dict = {}


def calculate_bmi(height_cm: float, weight_kg: float):

    bmi = weight_kg / ((height_cm / 100) ** 2)

    if bmi < 18.5:
        category = "UNDERWEIGHT"

    elif bmi < 25:
        category = "STANDARD"

    elif bmi < 30:
        category = "OVERWEIGHT"

    else:
        category = "OBESE"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }


@app.post("/mcp/invoke")
async def invoke_tool(request: MCPInvokeRequest):

    if request.tool_name != "calculate_bmi":

        return {
            "error":
            f"Unknown tool: {request.tool_name}"
        }

    args = request.arguments

    result = calculate_bmi(
        height_cm=args.get("height_cm"),
        weight_kg=args.get("weight_kg")
    )

    return {
        "result": result
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )