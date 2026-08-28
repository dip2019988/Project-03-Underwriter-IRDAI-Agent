import uuid

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import settings
from data.generate_docs import main as generate_mock_docs
from graph.graph_builder import compiled_guarded_graph
from presidio_governance.anonymizer import presidio_anonymizer_service
from schemas.api_schemas import Token, UnderwritingRequest, UnderwritingResponse
from security.auth import (
    MOCK_USER_DB,
    create_access_token,
    verify_password,
)
from security.rbac import require_advisor_or_underwriter
from services.memory_service import mem0_service
from services.redis_service import redis_service
from utils.logger import logger

app = FastAPI(

    title=f"{settings.PROJECT_NAME} API",

    version=settings.VERSION,

    description=(
        "IRDAI-Compliant Life Insurance "
        "Underwriting API powered by "
        "LangGraph, Presidio, Mem0, "
        "MCP Tools and Guardrails."
    ),

    docs_url="/docs",

    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():

    logger.info(
        "[API] Starting Insurance Underwriting API"
    )

    if not settings.KB_FILE_PATH.exists():
        generate_mock_docs()


@app.on_event("shutdown")
def shutdown_event():

    logger.info(
        "[API] Shutdown initiated"
    )

    if hasattr(mem0_service, "close"):
        mem0_service.close()


# --------------------------------------------------
# AUTH
# --------------------------------------------------

@app.post(
    "/api/v1/auth/login",
    response_model=Token,
    tags=["Authentication"]
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = MOCK_USER_DB.get(
        form_data.username
    )

    if (
        not user
        or not verify_password(
            form_data.password,
            user["hashed_password"]
        )
    ):
        raise HTTPException(

            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Incorrect username or password"
        )

    access_token = create_access_token(

        data={
            "sub": user["username"],
            "role": user["role"]
        }
    )

    return Token(

        access_token=access_token,

        token_type="bearer",

        expires_in_minutes=
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


# --------------------------------------------------
# UNDERWRITING API
# --------------------------------------------------

@app.post(
    "/api/v1/underwriting/evaluate",
    response_model=UnderwritingResponse,
    tags=["Insurance Underwriting"]
)
async def evaluate_underwriting(

    request: UnderwritingRequest,

    current_user: dict = Depends(
        require_advisor_or_underwriter
    )
):

    customer_name = current_user["username"]

    customer_id = request.customer_id

    thread_id = str(
        uuid.uuid4()
    )[:8]

    sanitized_query, _ = (
        presidio_anonymizer_service
        .anonymize_and_map(
            request.raw_query
        )
    )

    cached_payload = (
        redis_service.get_cached_solution(
            sanitized_query,
            customer_id
        )
    )


    if cached_payload:

        return UnderwritingResponse(

            thread_id=thread_id,

            customer_name=customer_name,

            customer_id=customer_id,

            intent=
            cached_payload.get(
                "intent",
                "GENERAL"
            ),

            sub_category=
            cached_payload.get(
                "sub_category",
                ""
            ),

            guardrail_passed=True,

            sanitized_query=
            cached_payload.get(
                "sanitized_query",
                request.raw_query
            ),

            solution=
            cached_payload.get(
                "solution",
                ""
            ),

            confidence_score=
            cached_payload.get(
                "confidence_score",
                100
            ),

            risk_category=
            cached_payload.get(
                "risk_category"
            ),

            underwriting_recommendation=
            cached_payload.get(
                "underwriting_recommendation"
            ),

            is_cached_response=True,

            visited_nodes=[
                "REDIS_CACHE_HIT"
            ]
        )

    customer_memory = (
        mem0_service
        .get_customer_memories(
            customer_id
        )
    )

    initial_state = {

        "customer_id":
            customer_id,

        "customer_name":
            customer_name,

        "raw_query":
            request.raw_query,

        "sanitized_query":
            "",

        "presidio_token_map":
            {},

        "customer_memory":
            customer_memory,

        "customer_profile":
            {},

        "financial_profile":
            {},

        "medical_profile":
            {},

        "family_profile":
            {},

        "intent":
            "GENERAL",

        "sub_category":
            "",

        "retrieved_docs":
            [],

        "bmi_result":
            {},

        "hlv_result":
            {},

        "premium_quote":
            {},

        "ulip_illustration": {},

        "risk_score":
            0,

        "risk_category":
            "",

        "solution":
            "",

        "underwriting_recommendation":
            "",

        "guardrail_passed":
            True,

        "guardrail_violation_reason":
            "",

        "confidence_score":
            0,

        "human_approved":
            False,

        "human_feedback":
            "",

        "is_cached_response":
            False,

        "retry_count":
            0,

        "visited_nodes":
            ["START"],

        "execution_logs": [
            "Insurance API request started"
        ]
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        final_state = (
            compiled_guarded_graph.invoke(
                initial_state,
                config=config
            )
        )

    except Exception as e:

        raise HTTPException(

            status_code=
            status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=
            f"LangGraph error: {e!s}"
        )

    if (

        final_state.get(
            "guardrail_passed",
            True
        )

        and

        final_state.get(
            "confidence_score",
            0
        ) >= settings.CONFIDENCE_THRESHOLD
    ):

        redis_service.set_cached_solution(
            final_state.get("sanitized_query",request.raw_query),
            customer_id,
            final_state
        )

        mem0_service.add_customer_memory(
            customer_id,
            final_state.get("sanitized_query", request.raw_query)
        )

    return UnderwritingResponse(

        thread_id=thread_id,

        customer_name=customer_name,

        customer_id=customer_id,

        intent=
        final_state.get(
            "intent",
            "GENERAL"
        ),

        sub_category=
        final_state.get(
            "sub_category",
            ""
        ),

        guardrail_passed=
        final_state.get(
            "guardrail_passed",
            True
        ),

        guardrail_violation_reason=
        final_state.get(
            "guardrail_violation_reason"
        ),

        sanitized_query=
        final_state.get(
            "sanitized_query",
            request.raw_query
        ),

        solution=
        final_state.get(
            "solution",
            ""
        ),

        confidence_score=
        final_state.get(
            "confidence_score",
            0
        ),

        risk_category=
        final_state.get(
            "risk_category"
        ),

        underwriting_recommendation=
        final_state.get(
            "underwriting_recommendation"
        ),

        is_cached_response=False,

        visited_nodes=
        final_state.get(
            "visited_nodes",
            []
        )
    )


@app.get(
    "/api/v1/health",
    tags=["Health"]
)
async def health_check():

    return {

        "status": "online",

        "redis_connected":
            redis_service.is_connected,

        "version":
            settings.VERSION
    }


if __name__ == "__main__":

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )