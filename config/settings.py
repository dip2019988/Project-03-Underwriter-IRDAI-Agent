import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=env_path
    if env_path.exists()
    else None
)


class Settings:

    PROJECT_NAME = (
        "Conversational Life Insurance "
        "Underwriter Agent"
    )

    VERSION = "1.0.0"

    # ----------------------------------
    # OpenAI
    # ----------------------------------

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_MODEL_NAME = os.getenv(
        "OPENAI_MODEL_NAME",
        "gpt-4o-mini"
    )

    TEMPERATURE = float(
        os.getenv(
            "TEMPERATURE",
            "0.1"
        )
    )

    # ----------------------------------
    # LangSmith
    # ----------------------------------

    LANGCHAIN_TRACING_V2 = os.getenv(
        "LANGCHAIN_TRACING_V2",
        "true"
    )

    LANGCHAIN_API_KEY = os.getenv(
        "LANGCHAIN_API_KEY",
        ""
    )

    LANGCHAIN_PROJECT = os.getenv(
        "LANGCHAIN_PROJECT",
        "Insurance-Underwriting-Agent"
    )

    # ----------------------------------
    # Agent Controls
    # ----------------------------------

    MAX_RETRY_COUNT = 2

    CONFIDENCE_THRESHOLD = 80

    # ----------------------------------
    # Redis
    # ----------------------------------

    REDIS_HOST = os.getenv(
        "REDIS_HOST",
        "localhost"
    )

    REDIS_PORT = int(
        os.getenv(
            "REDIS_PORT",
            "6379"
        )
    )

    REDIS_PASSWORD = os.getenv(
        "REDIS_PASSWORD",
        ""
    )

    REDIS_CACHE_TTL = int(
        os.getenv(
            "REDIS_CACHE_TTL",
            "3600"
        )
    )

    # ----------------------------------
    # Mem0
    # ----------------------------------

    MEM0_API_KEY = os.getenv(
        "MEM0_API_KEY",
        ""
    )

    # ----------------------------------
    # Insurance MCP Services
    # ----------------------------------

    MCP_BMI_URL = os.getenv(
        "MCP_BMI_URL",
        "http://localhost:8001"
    )

    MCP_HLV_URL = os.getenv(
        "MCP_HLV_URL",
        "http://localhost:8002"
    )

    MCP_PREMIUM_URL = os.getenv(
        "MCP_PREMIUM_URL",
        "http://localhost:8003"
    )

    # ----------------------------------
    # Security
    # ----------------------------------

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "insurance-secret-key"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = 480

    # ----------------------------------
    # Data Paths
    # ----------------------------------

    DATA_DIR = BASE_DIR / "data"

    KB_FILE_PATH = (
        DATA_DIR / "insurance_kb.json"
    )

    CUSTOMER_DATA_FILE = (
        DATA_DIR / "customer_profiles.json"
    )

    MEDICAL_DATA_FILE = (
        DATA_DIR / "medical_histories.json"
    )

    # ----------------------------------
    # Validation
    # ----------------------------------

    @classmethod
    def validate(cls):

        if (
            not cls.OPENAI_API_KEY
            or cls.OPENAI_API_KEY
            == "your_openai_api_key_here"
        ):

            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

    LOG_LEVEL = "INFO"


settings = Settings()