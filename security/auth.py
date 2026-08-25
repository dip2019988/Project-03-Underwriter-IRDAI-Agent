from datetime import datetime, timedelta
from typing import Optional

import jwt

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from config.settings import settings
from schemas.api_schemas import TokenData


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# --------------------------------------------------
# Mock Insurance Users
# --------------------------------------------------

MOCK_USER_DB = {

    "advisor01": {
        "username": "advisor01",
        "hashed_password": pwd_context.hash(
            "InsurancePass123!"
        ),
        "role": "advisor"
    },

    "underwriter01": {
        "username": "underwriter01",
        "hashed_password": pwd_context.hash(
            "UnderwriterPass123!"
        ),
        "role": "underwriter"
    }
}


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm="HS256"
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> dict:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if (
            username is None
            or username not in MOCK_USER_DB
        ):
            raise credentials_exception

        token_data = TokenData(
            username=username,
            role=role
        )

    except jwt.PyJWTError:

        raise credentials_exception

    return MOCK_USER_DB[
        token_data.username
    ]